import pymysql
import json

class DatabaseConnection:
    def __init__(self):
        try:
            """Load database configuration from a JSON file"""
            with open('config.json','r') as config_file:
                self.config = json.load(config_file)

            """Establish a connection to the database using the configuration"""
            self.connection = pymysql.connect(
                host=self.config['MySQL']['server'],
                database=self.config['MySQL']['database'],
                user=self.config['MySQL']['username'],
                password=self.config['MySQL']['password']
            )

            """Create a cursor to execute SQL queries"""
            self.cursor = self.connection.cursor()
        except Exception as e:
            print("Error connecting to the database:", str(e))

    def connect(self):
        """Establish a database connection and return a session."""
        return self.cursor

    def close(self):
        """Close the database connection."""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'connection'):
            self.connection.close()

    def execute_query(self, query):
        """Execute a SQL query and return the result."""
        try:
            """Execute the SQL query and fetch the results"""
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None

    def execute_insert_query(self, query, values):
        """Execute a SQL query and return the result."""
        try:
            """Execute the INSERT SQL query with provided values"""
            self.cursor.execute(query, values)

        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None

    def commit(self):
        """Commit the current transaction."""
        try:
            """ Commit the changes to the database"""
            self.connection.commit()
        except Exception as e:
            print(f"Error committing transaction: {str(e)}")