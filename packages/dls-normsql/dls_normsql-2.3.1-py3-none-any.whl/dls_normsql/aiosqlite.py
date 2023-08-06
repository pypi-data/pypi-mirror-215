import asyncio
import glob

# This class produces log entries.
import logging
import os
import re
import shutil
from collections import OrderedDict
from datetime import datetime

import aiosqlite

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.explain import explain
from dls_utilpack.isodatetime import isodatetime_filename
from dls_utilpack.require import require

from dls_normsql.constants import CommonFieldnames, RevisionFieldnames, Tablenames
from dls_normsql.table_definition import TableDefinition

logger = logging.getLogger(__name__)

connect_lock = asyncio.Lock()
apply_revisions_lock = asyncio.Lock()


# ----------------------------------------------------------------------------------------
def sqlite_regexp_callback(pattern, input):
    reg = re.compile(pattern)
    return reg.search(input) is not None


# ----------------------------------------------------------------------------------------
class Aiosqlite:
    """
    Class with coroutines for creating and querying a sqlite database.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification, database_definition_object):
        """
        Construct object.  Do not connect to database.
        """
        self.__filename = require(
            f"{callsign(self)} specification", specification, "filename"
        )

        # Default is an empty type_specific_tbd.
        self.__type_specific_tbd = specification.get("type_specific_tbd", {})

        # Backup directory default is the path where the filename is.
        self.__backup_directory = specification.get(
            "backup_directory", os.path.dirname(self.__filename)
        )

        # Don't normally want to see all the debug for aiosqlite internals.
        level = specification.get("log_level", "INFO")
        logging.getLogger("aiosqlite").setLevel(level)

        self.__connection = None

        self.__database_definition_object = database_definition_object

        self.__tables = {}

        self.__backup_restore_lock = asyncio.Lock()

        # Last undo position.
        self.__last_restore = 0

    # ----------------------------------------------------------------------------------------

    async def connect(self, should_drop_database=False):
        """
        Connect to database at filename given in constructor.
        """

        async with connect_lock:
            should_create_schemas = False

            # File doesn't exist yet?
            if not os.path.isfile(self.__filename):
                # Create directory for the file.
                await self.__create_directory(self.__filename)
                # After connection, we must create the schemas.
                should_create_schemas = True

            logger.debug(f"connecting to {self.__filename}")

            self.__connection = await aiosqlite.connect(self.__filename)
            self.__connection.row_factory = aiosqlite.Row

            await self.__connection.create_function("regexp", 2, sqlite_regexp_callback)

            # Let the base class contribute its table definitions to the in-memory list.
            await self.add_table_definitions()

            if should_create_schemas:
                await self.create_schemas()
                await self.insert(
                    Tablenames.REVISION,
                    [{"number": self.__database_definition_object.LATEST_REVISION}],
                )
                # TODO: Set permission on sqlite file from configuration.
                os.chmod(self.__filename, 0o666)

            # Emit the name of the database file for positive confirmation on console.
            logger.info(
                f"{callsign(self)} database file is {self.__filename} database definition revision {self.__database_definition_object.LATEST_REVISION}"
            )

    # ----------------------------------------------------------------------------------------
    async def apply_revisions(self):
        """
        Apply revision updates to databse if needed.
        """

        # TODO: Consider how to lock database while running applying_revisions.
        # TODO: Establish transaction arouund apply_revisions with rollback if error.
        async with apply_revisions_lock:
            try:
                records = await self.query(
                    f"SELECT number FROM {Tablenames.REVISION}",
                    why="get database revision",
                )
                if len(records) == 0:
                    database_revision = 0
                else:
                    database_revision = records[0]["number"]
            except Exception as exception:
                logger.warning(
                    f"could not get revision, presuming legacy database with no table: {exception}"
                )
                database_revision = 0

            if database_revision < self.__database_definition_object.LATEST_REVISION:
                # Backup before applying revisions.
                logger.debug(
                    f"[BKREVL] backing up before updating from database revision {database_revision}"
                    f" to definition revision {self.__database_definition_object.LATEST_REVISION}"
                )

                await self.backup()

                for revision in range(
                    database_revision, self.__database_definition_object.LATEST_REVISION
                ):
                    await self.apply_revision(revision + 1)
                await self.update(
                    Tablenames.REVISION,
                    {"number": self.__database_definition_object.LATEST_REVISION},
                    "1 = 1",
                    why="update database revision",
                )
            else:
                logger.debug(
                    f"[BKREVL] no need to update database revision {database_revision}"
                    f" which matches definition revision {self.__database_definition_object.LATEST_REVISION}"
                )

    # ----------------------------------------------------------------------------------------
    async def apply_revision(self, revision):
        logger.debug(f"updating to revision {revision}")
        # Updating to revision 1 presumably means
        # this is a legacy database with no revision table in it.
        if revision == 1:
            logger.info(f"creating {Tablenames.REVISION} table")
            await self.create_table(Tablenames.REVISION)
            await self.insert(Tablenames.REVISION, [{"revision": revision}])

        # Let the database definition object do its thing.
        await self.__database_definition_object.apply_revision(self, revision)

    # ----------------------------------------------------------------------------------------
    async def disconnect(self):

        if self.__connection is not None:
            # Commit any uncommitted transactions.
            await self.commit()

            logger.debug(f"[DISSHU] {callsign(self)} disconnecting")
            await self.__connection.close()
            self.__connection = None

    # ----------------------------------------------------------------------------------------
    async def __create_directory(self, filename):

        directory, filename = os.path.split(filename)

        if not os.path.exists(directory):
            # Make sure that parent directories which get created will have public permission.
            umask = os.umask(0)
            os.umask(umask & ~0o0777)
            os.makedirs(directory)
            os.umask(umask)

    # ----------------------------------------------------------------------------------------
    def add_table_definition(self, table_definition):

        self.__tables[table_definition.name] = table_definition

    # ----------------------------------------------------------------------------------------
    async def add_table_definitions(self):

        self.add_table_definition(RevisionTableDefinition(self))

        # Let the database definition object do its thing.
        await self.__database_definition_object.add_table_definitions(self)

    # ----------------------------------------------------------------------------------------
    async def begin(self):
        """
        Begin transaction.
        """

        # Close off any transactions underway.
        await self.__connection.commit()

        await self.__connection.execute("BEGIN")

    # ----------------------------------------------------------------------------------------
    async def commit(self):
        """
        Commit transaction.
        """

        await self.__connection.commit()

    # ----------------------------------------------------------------------------------------
    async def rollback(self):
        """
        Roll back transaction.
        """

        await self.__connection.rollback()

    # ----------------------------------------------------------------------------------------
    async def create_schemas(self):

        await self.begin()

        try:
            for table in self.__tables.values():
                await self.create_table(table)
            await self.commit()
        except Exception:
            await self.rollback()

    # ----------------------------------------------------------------------------------------
    async def create_table(self, table):
        """
        Wipe and re-create the table in the database.
        """

        # If table is a string, presume it's a table name.
        if isinstance(table, str):
            table = require("table definitions", self.__tables, table)

        await self.__connection.execute("DROP TABLE IF EXISTS %s" % (table.name))

        fields_sql = []
        indices_sql = []

        for field_name in table.fields:
            field = table.fields[field_name]
            fields_sql.append("`%s` %s" % (field_name, field["type"]))
            if field.get("index"):
                indices_sql.append(
                    "CREATE INDEX `%s_%s` ON `%s`(`%s`)"
                    % (table.name, field_name, table.name, field_name)
                )

        sql = "CREATE TABLE `%s`\n(%s)" % (table.name, ",\n  ".join(fields_sql))

        logger.debug("\n%s\n%s" % (sql, "\n".join(indices_sql)))

        await self.__connection.execute(sql)

        for sql in indices_sql:
            await self.__connection.execute(sql)

    # ----------------------------------------------------------------------------------------
    async def insert(
        self,
        table,
        rows,
        why=None,
    ) -> None:
        """
        Insert one or more rows.
        Each row is a dictionary.
        The first row is expected to define the keys for all rows inserted.
        Keys in the rows are ignored if not defined in the table schema.
        Table schema columns not specified in the first row's keys will get their sql-defined default values.
        """

        if len(rows) == 0:
            return

        # If table is a string, presume it's a table name.
        if isinstance(table, str):
            table = require("table definitions", self.__tables, table)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        values_rows = []

        insertable_fields = []
        for field in table.fields:
            # The first row is expected to define the keys for all rows inserted.
            if field in rows[0]:
                insertable_fields.append(field)
            elif field == CommonFieldnames.CREATED_ON:
                insertable_fields.append(field)

        qmarks = ["?"] * len(insertable_fields)

        for row in rows:
            values_row = []
            for field in table.fields:
                if field == CommonFieldnames.CREATED_ON:
                    created_on = row.get(field)
                    if created_on is None:
                        created_on = now
                    values_row.append(created_on)
                elif field in row:
                    values_row.append(row[field])
            values_rows.append(values_row)

        sql = "INSERT INTO %s\n  (%s)\n  VALUES (%s)" % (
            table.name,
            ", ".join(insertable_fields),
            ", ".join(qmarks),
        )

        try:
            await self.__connection.executemany(sql, values_rows)

            if why is None:
                logger.debug("\n%s\n%s" % (sql, values_rows))
            else:
                logger.debug("%s:\n%s\n%s" % (why, sql, values_rows))

        except aiosqlite.OperationalError:
            if why is None:
                raise RuntimeError(f"failed to execute {sql}")
            else:
                raise RuntimeError(f"failed to execute {why}: {sql}")

    # ----------------------------------------------------------------------------------------
    async def update(
        self,
        table,
        row,
        where,
        subs=None,
        why=None,
    ):
        """
        Update specified fields to all rows matching selection.
        """

        # If table is a string, presume it's a table name.
        if isinstance(table, str):
            table = require("table definitions", self.__tables, table)

        values_row = []
        qmarks = []

        for field in table.fields:
            if field == CommonFieldnames.UUID or field == CommonFieldnames.AUTOID:
                continue
            if field not in row:
                continue
            qmarks.append("%s = ?" % (field))
            values_row.append(row[field])

        if len(values_row) == 0:
            raise RuntimeError("no fields in record match database table")

        sql = "UPDATE %s SET\n  %s\nWHERE %s" % (
            table.name,
            ",\n  ".join(qmarks),
            where,
        )

        if subs is not None:
            values_row.extend(subs)

        try:
            cursor = await self.__connection.execute(sql, values_row)
            rowcount = cursor.rowcount

            if why is None:
                logger.debug(
                    "%d rows from:\n%s\nvalues %s" % (rowcount, sql, values_row)
                )
            else:
                logger.debug(
                    "%d rows from %s:\n%s\nvalues %s" % (rowcount, why, sql, values_row)
                )

        except aiosqlite.OperationalError:
            if why is None:
                raise RuntimeError(f"failed to execute {sql}")
            else:
                raise RuntimeError(f"failed to execute {why}: {sql}")

        return rowcount

    # ----------------------------------------------------------------------------------------
    async def execute(self, sql, subs=None, why=None):
        """
        Execute a sql statement.
        If subs is a list of lists, then these are presumed the values for executemany.
        """

        cursor = None
        try:
            # Subs is a list of lists?
            if isinstance(subs, list) and len(subs) > 0 and isinstance(subs[0], list):
                logger.debug(f"inserting {len(subs)} of {len(subs[0])}")
                cursor = await self.__connection.executemany(sql, subs)
            else:
                cursor = await self.__connection.execute(sql, subs)

            if why is None:
                if cursor.rowcount > 0:
                    logger.debug(
                        f"{cursor.rowcount} records affected by\n{sql} values {subs}"
                    )
                else:
                    logger.debug(f"{sql} values {subs}")
            else:
                if cursor.rowcount > 0:
                    logger.debug(
                        f"{cursor.rowcount} records affected by {why}:\n{sql} values {subs}"
                    )
                else:
                    logger.debug(f"{why}: {sql} values {subs}")
        except aiosqlite.OperationalError:
            if why is None:
                raise RuntimeError(f"failed to execute {sql}")
            else:
                raise RuntimeError(f"failed to execute {why}: {sql}")

    # ----------------------------------------------------------------------------------------
    def __format_debug(self, why, rows, sql, subs):
        parts = ""

        if rows is not None:
            parts += f"{len(rows)} records from"

        if why is not None:
            parts += " " + why

        if len(parts) > 0:
            parts += ": "

        parts += sql

        if subs is not None and len(subs) > 0:
            parts += "\n  "
            parts += str(subs)

        return parts

    # ----------------------------------------------------------------------------------------
    async def query(self, sql, subs=None, why=None):

        if subs is None:
            subs = {}

        cursor = None
        try:
            cursor = await self.__connection.cursor()
            await cursor.execute(sql, subs)
            rows = await cursor.fetchall()
            cols = []
            for col in cursor.description:
                cols.append(col[0])

            logger.debug(self.__format_debug(why, rows, sql, subs))

            records = []
            for row in rows:
                record = OrderedDict()
                for index, col in enumerate(cols):
                    record[col] = row[index]
                records.append(record)
            return records
        except aiosqlite.OperationalError as exception:
            if why is None:
                raise RuntimeError(explain(exception, f"executing {sql}"))
            else:
                raise RuntimeError(explain(exception, f"executing {why}: {sql}"))
        finally:
            if cursor is not None:
                await cursor.close()

    # ----------------------------------------------------------------------------------------
    async def backup(self):
        """
        Back up database to timestamped location.
        """

        async with self.__backup_restore_lock:
            # Prune all the restores which were orphaned.
            directory = self.__backup_directory
            if directory is None:
                raise RuntimeError("no backup directory supplied in confirmation")

            basename, suffix = os.path.splitext(os.path.basename(self.__filename))

            filenames = glob.glob(f"{directory}/{basename}.*{suffix}")

            filenames.sort(reverse=True)

            for restore in range(self.__last_restore):
                logger.debug(
                    f"[BACKPRU] removing {restore}-th restore {filenames[restore]}"
                )
                os.remove(filenames[restore])

            self.__last_restore = 0

            timestamp = isodatetime_filename()
            to_filename = f"{directory}/{basename}.{timestamp}{suffix}"

            await self.disconnect()
            try:
                await self.__create_directory(to_filename)
                shutil.copy2(self.__filename, to_filename)
                logger.debug(f"backed up to {to_filename}")
            except Exception:
                raise RuntimeError(f"copy {self.__filename} to {to_filename} failed")
            finally:
                await self.connect()

    # ----------------------------------------------------------------------------------------
    async def restore(self, nth):
        """
        Restore database from timestamped location.
        """

        async with self.__backup_restore_lock:
            directory = self.__backup_directory
            if directory is None:
                raise RuntimeError("no backup directory supplied in confirmation")

            basename, suffix = os.path.splitext(os.path.basename(self.__filename))

            filenames = glob.glob(f"{directory}/{basename}.*{suffix}")

            filenames.sort(reverse=True)

            if nth >= len(filenames):
                raise RuntimeError(
                    f"restoration index {nth} is more than available {len(filenames)}"
                )

            from_filename = filenames[nth]

            await self.disconnect()
            try:
                shutil.copy2(from_filename, self.__filename)
                logger.debug(
                    f"restored nth {nth} out of {len(filenames)} from {from_filename}"
                )
            except Exception:
                raise RuntimeError(f"copy {from_filename} to {self.__filename} failed")
            finally:
                await self.connect()

            self.__last_restore = nth


# ----------------------------------------------------------------------------------------
class RevisionTableDefinition(TableDefinition):
    # ----------------------------------------------------------------------------------------
    def __init__(self, database):
        TableDefinition.__init__(self, "revision")

        self.fields[RevisionFieldnames.CREATED_ON] = {"type": "TEXT", "index": True}
        self.fields[RevisionFieldnames.NUMBER] = {"type": "INTEGER", "index": False}
