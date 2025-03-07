import configparser
import mysql.connector
from mysql.connector import Error

from static.sql_parser import SQLParser
from static.error_handler import ErrorHandler


class Config:
    def __init__(self, config_file='config.properties'):
        """Initialize Config object and read configuration file."""
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.config_file)
        except Exception as e:
            # Handle error reading the config file
            self.error_message = ErrorHandler.handle_error(e, "Error reading configuration file")

    def _get_db_config(self):
        """Helper function to get database configuration from the config file."""
        try:
            db = self.config['database']
            return {
                'host': db.get('host'),
                'user': db.get('user'),
                'password': db.get('password'),
                'database': db.get('database')  # This is used later when the database exists
            }
        except KeyError as e:
            # Create an instance of the ErrorHandler class
            error_handler = ErrorHandler()
            # Handle missing config keys
            self.error_message = error_handler.handle_config(e, context="Missing required database configuration")
            raise ValueError(f"Missing required database config: {e}")

    def get_db_connection(self, initial=False):
        """Establish and return a database connection."""
        db_config = self._get_db_config()

        # If a database is provided, use it, otherwise, connect without specifying a database
        connection_params = {
            'host': db_config['host'],
            'user': db_config['user'],
            'password': db_config['password']
        }

        # This sets db to None if initial is True, else it fetches the database name from the config
        database = None if initial is True else self.config['database']['database']

        # Ensure the database is selected if it's provided
        if database:
            connection_params['database'] = database

        try:
            connection = mysql.connector.connect(**connection_params)
            if connection.is_connected():
                return connection
            else:
                raise ConnectionError("Failed to establish database connection.")
        except Error as e:
            # Create an instance of the ErrorHandler class
            error_handler = ErrorHandler()
            # Handle connection errors
            self.error_message = error_handler.handle_config(e, context="Error connecting to the database")
            raise ConnectionError(f"Error connecting to database: {e}")
        except Exception as e:
            # Create an instance of the ErrorHandler class
            error_handler = ErrorHandler()
            # Catch any other general errors
            self.error_message = error_handler.handle_config(e, context="General database connection error")
            raise

    def get_db_cursor(self, initial=False):
        """
            Create and return a database cursor that returns
            rows as dictionaries instead of lists of Tuples.
        """
        try:
            connection = self.get_db_connection(initial)
            cursor = connection.cursor(dictionary=True)  # Use dictionary=True for dict output (override Tuple output)
            return cursor, connection
        except Exception as e:
            error_handler = ErrorHandler()
            # Handle error while getting cursor
            self.error_message = error_handler.handle_config(e, context="Error creating database cursor")
            raise

    def close_db_connection(self, connection):
        """Close the database connection."""
        if connection and connection.is_connected():
            connection.close()

    def close_db_cursor(self, cursor):
        """Close the database cursor."""
        if cursor:
            cursor.close()

    def execute_query(self, query, params=None):
        """Execute a single query (SELECT or non-SELECT)."""
        conn = None
        cursor = None
        result = None
        error = None

        try:
            cursor, conn = self.get_db_cursor()

            # If there are parameters, use them; otherwise, just execute the query directly
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)  # Execute the query without parameters

            # If it's a SELECT query, fetch the results
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()  # Fetch the results for SELECT queries
                print(f"Fetched results: {result}")

            # For non-SELECT queries, return the number of affected rows
            else:
                result = cursor.rowcount  # Return number of rows affected
                print(f"Affected rows: {result}")

            # Ensure any previous result sets are consumed, if applicable to avoid error: Unread result
            if cursor.nextset():
                cursor.fetchall()  # Consume any other result sets

            # Commit for non-SELECT queries (e.g., INSERT, UPDATE, CREATE DATABASE)
            conn.commit()

        except Error as e:
            # Handle query execution errors
            error_handler = ErrorHandler()
            self.error_message = error_handler.handle_config(e, context="Error executing database query")
            result = None

        finally:
            if cursor is not None:
                self.close_db_cursor(cursor)
            if conn is not None:
                self.close_db_connection(conn)

        return result

    # CREATE DATABASE
    def check_and_create_database(self):
        """Check if the database exists, if not, create it."""
        conn = None
        cursor = None

        try:
            # Direct connection to MySQL server (do not specify a database)
            cursor, conn = self.get_db_cursor(True)
            db_config = self._get_db_config()
            database_name = db_config['database']  # Get the database name from config

            # Check if the database exists
            check_db_query = f"SHOW DATABASES LIKE '{database_name}'"
            cursor.execute(check_db_query)
            result = cursor.fetchone()

            if result:
                print(f"Database '{database_name}' already exists.")
            else:
                # If the database does not exist, create it
                create_db_query = f"CREATE DATABASE `{database_name}`"
                cursor.execute(create_db_query)
                print(f"Database '{database_name}' created successfully.")

            # Commit the transaction (optional for DDL queries, but included for consistency)
            conn.commit()

        except Error as e:
            error_handler = ErrorHandler()
            # Handle database creation errors
            self.error_message = error_handler.handle_config(e, context="Error checking or creating database")

        finally:
            # Ensure resources are cleaned up after the operation
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def drop_database(self):
        db_config = self._get_db_config()
        database_name = db_config['database']
        drop_query = f'DROP DATABASE IF EXISTS {database_name}'

        return self.execute_query(drop_query)

    def reset_database(self):
        self.drop_database()
        self.check_and_create_database()
        self.check_and_create_tables()

    def get_db_schema_names(self, database_name):
        select_query = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.tables WHERE TABLE_SCHEMA = '{database_name}'"
        table_names = self.execute_query(select_query)
        return table_names

    # CREATE TABLES
    def check_and_create_tables(self):
        """Check if tables exist, and create them if necessary."""
        conn = None
        cursor = None

        try:
            # Get connection to the MySQL server
            db_config = self._get_db_config()
            # Get the database cursor and connection
            cursor, conn = self.get_db_cursor()

            # Get a list of existing tables from the specified database
            database_name = db_config['database']

            table_names = self.get_db_schema_names(database_name)

            print(f"Existing tables: {table_names}")

            # Check if tables need to be created
            # For this example, we're assuming that if no tables exist, we need to create them
            if not table_names:
                print("No tables found. Creating tables...")
                # Read the SQL file and execute the queries
                with open('static/create_tables.sql', 'r') as f:
                    # cursor.execute(): doesn't support executing multiple SQL statements at once with the multi=True parameter in MySQL
                    # cursor.execute(f.read(), multi=True)
                    sql = f.read()

                    # DROP DATABASE _degree_evaluation;

                    # Split SQL file by semicolons, but handle each statement correctly
                    sql_statements = sql.split(';')  # Split by semicolon to separate the SQL statements
                    for statement in sql_statements:
                        statement = statement.strip()  # Remove extra spaces/newlines
                        if statement:  # Ensure the statement is not empty
                            self.execute_query(statement)  # Execute each statement individually
                            table_name = SQLParser.extract_schema_and_table(
                                statement)  # The table name is in the first column of the result
                            print(f"Table Created -> {table_name} <-")

                print("Tables creation was successful.")
            else:
                print("Tables already exist. Skipping table creation.")

        except Error as e:
            error_handler = ErrorHandler()
            self.error_message = error_handler.handle_config(e, context="Error checking or creating tables")

        finally:
            # Ensure resources are cleaned up after the operation
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # DROP TABLES
    def drop_tables(self):
        """Drop tables if they exist."""
        conn = None
        cursor = None

        try:
            # Get connection to the MySQL server
            cursor, conn = self.get_db_cursor()
            db_config = self._get_db_config()

            # Get the list of existing tables from the specified database
            database_name = db_config['database']  # Get database name from config

            table_names = self.get_db_schema_names(database_name)

            if not table_names:
                print("No tables found to drop.")
                return

            print(f"Existing tables to drop: {table_names}")

            # Drop each table
            for table in table_names:
                table_name = table['TABLE_NAME']  # The table name is in the first column of the result
                drop_query = f"DROP TABLE IF EXISTS `{table_name}`"
                self.execute_query(drop_query)
                print(f"Dropped table: {table_name}")

            print("All specified tables have been dropped successfully.")

        except Error as e:
            error_handler = ErrorHandler()
            self.error_message = error_handler.handle_config(e, context="Error dropping tables")

        finally:
            # Ensure resources are cleaned up after the operation
            if cursor:
                cursor.close()
            if conn:
                conn.close()
