import pymysql
import json

# Function to delete records based on filename
def delete_records_by_filename(connection, table_name, filenames):
    try:
        with connection.cursor() as cursor:
            # Generate the SQL query to delete the records
            sql_query = f"DELETE FROM {table_name} WHERE filename IN (%s)"
            # Execute the query for the provided filenames
            cursor.executemany(sql_query, [(filename,) for filename in filenames])
            # Commit the transaction
            connection.commit()
            print(f"Deleted records for filenames: {filenames}")
    except Exception as e:
        print(f"Error while deleting records: {e}")
        connection.rollback()

# Establish RDS connection
def connect_to_rds(username, password, host, database, port=3306):
    try:
        connection = pymysql.connect(
            user=username,
            password=password,
            host=host,
            database=database,
            port=port,
        )
        return connection
    except Exception as e:
        print(f"Error connecting to RDS: {e}")
        return None

# Define RDS credentials and target table/filenames
rds_credentials = {
    "username": "your_rds_username",
    "password": "your_rds_password",
    "host": "your_rds_endpoint",
    "database": "your_rds_database",
    "port": 3306,  # Default MySQL port
}
table_name = "your_table_name"
filenames_to_delete = [
    "",
    "",
    # Add other filenames here
]

# Main Execution
if __name__ == "__main__":
    connection = connect_to_rds(
        rds_credentials["username"],
        rds_credentials["password"],
        rds_credentials["host"],
        rds_credentials["database"],
        rds_credentials["port"],
    )
    if connection:
        delete_records_by_filename(connection, table_name, filenames_to_delete)
        connection.close()
