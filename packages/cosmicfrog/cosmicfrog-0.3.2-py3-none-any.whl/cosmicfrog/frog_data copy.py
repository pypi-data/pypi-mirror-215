import pandas as pd
import numpy as np
import json
import os
import sqlalchemy
from sqlalchemy import text, MetaData, inspect
from sqlalchemy.engine import Engine
from psycopg2 import sql
import uuid
from io import StringIO
from typing import Type
from collections.abc import Iterable
import pkg_resources

from .frog_log import get_logger

# Questions: 
# How to support feedback in CF UI?

# TODO: 
# Will need extending to support custom columns in Anura tables
# Will need extensions for custom tables in a model
# Profile parallel write for xlsx
# Test sql injection
# Add batching to standard table writing

# Define chunk size (number of rows to write per chunk)
UPSERT_CHUNK_SIZE = 10000

MASTER_LIST_PATH = 'anura/table_masterlists/anuraMasterTableList.json'
TABLES_DIR = 'anura/table_definitions'

class ValidationError(Exception):
    """Exception raised for validation errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class frog_model:

    anura_tables = []
    anura_keys = {}
    anura_cols = {}

    @classmethod
    def _read_anura(cls: Type['frog_model']):
        frog_model._read_tables()
        frog_model._read_pk_columns()

    
    @classmethod
    def _read_tables(cls: Type['frog_model']):

        file_path = pkg_resources.resource_filename(__name__, MASTER_LIST_PATH)
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            frog_model.anura_tables = [item["Table"].lower() for item in data]


    @classmethod 
    def _read_pk_columns(cls: Type['frog_model']):

        file_path = pkg_resources.resource_filename(__name__, TABLES_DIR)

        # Iterate over each file in the directory
        for filename in os.listdir(file_path):

            filepath = os.path.join(file_path, filename)

            with open(filepath, 'r') as f:
                data = json.load(f)
                
            table_name = data.get("TableName").lower()
            
            # Extract the column names where "PK" is "Yes"
            all_columns = [field["Column Name"].lower() for field in data.get("fields", [])]
            pk_columns = [field["Column Name"].lower() for field in data.get("fields", []) if field.get("PK") == "Yes"]
            
            frog_model.anura_cols[table_name] = all_columns
            frog_model.anura_keys[table_name] = pk_columns


    def __init__(self, connection_string: str = None, engine: sqlalchemy.engine.Engine = None) -> None:

        self.engine = None
        self.connection = None
        self.transaction = None
        self.log = get_logger()

        # One time read in of Anura data
        if not frog_model.anura_tables:
            self.log.info("Reading Anura schema")
            frog_model._read_anura()

        # Initialise connection
        if engine is not None:
            self.engine = engine
        elif connection_string is not None:
            self.engine = sqlalchemy.create_engine(connection_string, connect_args={'connect_timeout': 15}) 

        if self.engine is not None:
            self.connection = self.engine.connect()


    def start_transaction(self):
        assert(self.connection is not None)
        self.transaction = self.connection.begin()


    def commit_transaction(self):
        self.transaction.commit()
        self.transaction = None


    def rollback_transaction(self):
        self.transaction.rollback()
        self.transaction = None


    def write_table(self, table_name: str, data: pd.DataFrame | Iterable):
        
        self.log.info("Writing table: " + table_name)

        if isinstance(data, pd.DataFrame) == False:
            data = pd.DataFrame(data)

        # Initial implementation - pull everything into a df and dump with to_sql
        data.to_sql(table_name, con=self.engine, if_exists="append", index=False)

        # Note: tried a couple of ways to dump the generator rows directly, but didn't
        # give significant performance over dataframe (though may be better for memory)
        # Decided to leave as is for now 


    def read_table(self, table_name: str):
        return pd.read_sql(table_name, self.engine)

    def clear_table(self, table):

        assert(self.connection is not None)

        # delete any existing data data from the table
        self.connection.execute(text("delete from " + table))

        return True

    def exec_sql(self, sql: str):

        assert(self.connection is not None)

        self.connection.execute(text(sql))

    def get_dataframe(self, sql: str):

        return pd.read_sql_query(sql, self.engine)

    # Upsert from a file
    def upsert_csv(self, table_name: str, filename: str):

        for chunk in pd.read_csv(filename, chunksize=UPSERT_CHUNK_SIZE, dtype=str, skipinitialspace=True):
            chunk.columns = chunk.columns.str.lower().map(str.strip)
            chunk.replace("", np.nan, inplace=True)
            self.upsert(table_name, chunk)
            break

    # Upsert from an xls
    def upsert_excel(self, filename: str):

        # TODO: If an issue could consider another way to load/stream from xlsx maybe?

        xls = pd.ExcelFile(filename)

        # For each sheet in the file
        for sheet_name in xls.sheet_names:

            # read the entire sheet into a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)

            df.columns = df.columns.str.lower().map(str.strip)

            for i in range(0, len(df), UPSERT_CHUNK_SIZE):
                chunk = df[i:i+UPSERT_CHUNK_SIZE]
                chunk.replace("", np.nan, inplace=True)
                self.upsert(sheet_name, chunk)

    # Upsert from a dataframe
    def upsert(self, table_name: str, data: pd.DataFrame | Iterable):

        print ("upsert called")

        # TODO: Not sure what validation to do here
        # TODO: Anura only, or custom tables?  (can pass in keys for those)
        # TODO: Custom columns and how to handle
        # TODO: up front validation, what are the rules?

        table_name = table_name.strip().lower()

        if table_name not in frog_model.anura_tables:
            #Skip it
            self.log.warning(f"""Worksheet name not recognised as Anura table (skipping): {table_name}""")
            return

        self.log.info(f"""Importing worksheet to table: {table_name}""")   

        #TODO: Will need more code for handling custom columns here, behavior should be:
        # Key columns - get used to match (Note: possible future requirement, some custom columns may also be key columns)
        # Other Anura columns - get updated
        # Other Custom columns - get updated
        # Other columns (neither Anura or Custom) - get ignored

        # Skipping unrecognised rows (note: does not support custom columns yet)

        self.log.info(f"""Found {len(frog_model.anura_cols[table_name])} columns""")

        cols_to_drop = [col for col in data.columns if col not in frog_model.anura_cols[table_name]]
        for col in cols_to_drop:
            self.log.info(f"""Skipping unknown column: {col}""")
        data.drop(cols_to_drop, axis=1, inplace=True)
         
        key_columns = frog_model.anura_keys[table_name]
        non_key_columns = [col for col in data.columns if col not in key_columns]
        all_columns = key_columns + non_key_columns

        assert(self.connection is not None)

        temp_table_name = "temp_table_" + str(uuid.uuid4()).replace('-', '')

        with self.engine.begin() as connection:
        
            self.log.info(f"""Moving data to temporary table: {temp_table_name}""")   

            # Create temporary table
            # Note: this will also clone custom columns
            create_temp_table_sql = text(f"""
                CREATE TEMPORARY TABLE {temp_table_name} AS
                SELECT *
                FROM {table_name}
                WITH NO DATA;
                """)
            
            connection.execute(create_temp_table_sql)   

            # Copy data from df to temporary table
            copy_sql = sql.SQL("COPY {table} ({fields}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)").format(
                table=sql.Identifier(temp_table_name),
                fields=sql.SQL(', ').join(map(sql.Identifier, data.columns))
            )

            cursor = connection.connection.cursor()
            cursor.copy_expert(copy_sql, StringIO(data.to_csv(index=False)))
            del data
            self.log.info(f"""Temporary table populated.""")   


            # Get all columns from the target table directly (allowing for custom columns)
            metadata = MetaData()

            # Create an Inspector object
            inspector = inspect(self.engine)

            # Get the column names for a specific table
            column_names = inspector.get_columns(table_name)
            target_table_column_names = [column['name'] for column in column_names]

            # Print the column names
            print("Target columns: {0}".format(target_table_column_names))

            target_table_column_names.remove("id")

            # Now upsert from temporary table to final table

            # Note: Looked at ON CONFLICT for upsert here, but seems not possible without defining constraints on target table
            # so doing insert and update separately

            # Note: For SQL injection, columns here are from Anura, also target table name. Temp table name is above.
            # non_key_columns are vulnerable (from import) so protected

            # Do not trust column names from user:
            safe_all_columns_list = sql.SQL(", ").join([sql.Identifier(col_name) for col_name in all_columns])
            safe_update_column_clause = sql.SQL(", ").join([sql.SQL('{0} = {1}.{0}').format(sql.Identifier(col_name), sql.Identifier(temp_table_name)) for col_name in non_key_columns])

            if key_columns:

                placeholder = "{0}"

                ############## UPDATE

                update_key_condition = " AND ".join([f"{table_name}.{key_col} = {temp_table_name}.{key_col}" for key_col in key_columns])

                update_query = sql.SQL(f"""
                    UPDATE {table_name}
                    SET {placeholder}
                    FROM {temp_table_name}
                    WHERE {update_key_condition}
                """).format(safe_update_column_clause)

                self.log.info(f"""Running (upsert) update query.""")  
                cursor.execute(update_query)
                updated_rows = cursor.rowcount


                ############## INSERT

                # insert_query = sql.SQL(f"""
                #     INSERT INTO {table_name} ({placeholder})
                #     SELECT {placeholder} FROM {temp_table_name}
                #     WHERE NOT EXISTS (
                #         SELECT 1 FROM {table_name}
                #         WHERE {key_condition}
                #     )
                # """).format(safe_all_columns_list)

                select_columns = ', '.join([f'{col}' for col in target_table_column_names])
                temp_select_columns = ', '.join([f'temp.{col}' for col in target_table_column_names])
                key_condition = " AND ".join([f"main.{key_col} = temp.{key_col}" for key_col in key_columns])
                null_condition = " AND ".join([f"main.{key_col} IS NULL" for key_col in key_columns])

                insert_query = sql.SQL(f"""
                    INSERT INTO {table_name} ({select_columns})
                    SELECT {temp_select_columns} FROM {temp_table_name} AS temp
                    LEFT JOIN {table_name} AS main ON {key_condition}
                    WHERE {null_condition}
                """).format(safe_all_columns_list)



                self.log.info(f"""Running (upsert) insert query.""")  
                cursor.execute(insert_query)
                inserted_rows = cursor.rowcount 

            else:
                self.log.info(f"""Running insert query.""")  
                insert_query = sql.SQL(f"""
                    INSERT INTO {table_name} ({placeholder})
                    SELECT {placeholder} FROM {temp_table_name}
                """).format(safe_all_columns_list)
                
                updated_rows = 0
                cursor.execute(insert_query)
                inserted_rows = cursor.rowcount 
                
                connection.execute(insert_query)

        #TODO: Could return this?
        self.log.info("Updated rows  = {}".format(updated_rows))
        self.log.info("Inserted rows = {}".format(inserted_rows))