import re

class SQLParser:

    # Extract Schema/Table name from SQL Statement
    def extract_schema_and_table(sql_statement):
        # Check if the schema starts with "CREATE TABLE"
        if not sql_statement.strip().startswith("CREATE TABLE"):
            return None, None

        # Clean the SQL statement to remove any unnecessary parts (like ENGINE)
        sql_statement_cleaned = re.sub(r"\s+ENGINE\s*=\s*\w+", "", sql_statement.strip(), flags=re.IGNORECASE)

        # Regex pattern to match the schema and table name in a CREATE TABLE statement
        # Adjusted pattern to allow optional schema and handle whitespace
        pattern = r'CREATE TABLE\s+([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)?)\s*\('

        # Search for the pattern in the cleaned SQL statement
        match = re.search(pattern, sql_statement_cleaned, re.IGNORECASE)

        if match:
            schema_and_table = match.group(1)

            if schema_and_table:
                # If a schema is provided (e.g., 'schema_name.table_name')
                if '.' in schema_and_table:
                    schema, table = schema_and_table.split('.')
                    print(f"Schema: {schema}")
                    print(f"Table: {table}")
                    return schema, table
                else:
                    # No schema, only table name
                    return None, schema_and_table
        return None, None

    # Extract Schema/Table name from SQL Statement
    def get_schema_from_statement(statement):
        """Extract the table name from a CREATE TABLE SQL statement."""

        # Strip any leading/trailing whitespace from the statement
        statement = statement.strip()

        # Regex pattern to match table name after CREATE TABLE and before parentheses
        pattern = r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([a-zA-Z0-9_]+)`?"

        # Search for the pattern
        match = re.match(pattern, statement, re.IGNORECASE)

        if match:
            return match.group(1)  # Return the table name
        else:
            return None  # Return None if the table name couldn't be found

