import pymysql
import boto3
import json

# AWS Region and Secret Manager Details
aws_region = 'eu-west-2'
secret_name = 'rds:cluster-7d6490f4-42f2-4cb7-891c-946b640be8ed'
rds_cluster_endpoint = 'sb-udv3-tenant-06524939-ingestion.cluster-cshv5uhk4xst.eu-west-2.rds.amazonaws.com'
database_name = 'udv3db'

# Function to retrieve RDS credentials
def get_rds_credentials(secret_name, region_name):
    client = boto3.client('secretsmanager', region_name=region_name)
    try:
        secret_response = client.get_secret_value(SecretId=secret_name)
        secret_data = json.loads(secret_response['SecretString'])
        return {
            'username': secret_data['username'],
            'password': secret_data['password'],
            'host': rds_cluster_endpoint,
            'port': secret_data.get('port', 3306)
        }
    except Exception as e:
        print(f"Error retrieving RDS credentials: {e}")
        return None

# Function to delete records based on filename
def delete_records_by_filename(credentials, table_name, filenames):
    try:
        # Establishing RDS connection
        connection = pymysql.connect(
            user=credentials['username'],
            password=credentials['password'],
            host=credentials['host'],
            database=database_name,
            port=credentials['port']
        )
        with connection.cursor() as cursor:
            # SQL query to delete records
            sql_query = f"DELETE FROM {table_name} WHERE filename = %s"
            for filename in filenames:
                cursor.execute(sql_query, (filename,))
            connection.commit()
            print(f"Deleted records for filenames: {filenames}")
    except Exception as e:
        print(f"Error while deleting records: {e}")
    finally:
        if connection:
            connection.close()

# Main Execution
if __name__ == "__main__":
    # Fetch RDS credentials
    rds_credentials = get_rds_credentials(secret_name, aws_region)
    if rds_credentials:
        # Define table name and filenames to delete
        table_name = "your_table_name"  # Replace with your actual table name
        filenames_to_delete = [
            "7122 WD-PIP-UK-BHR.pdf",
            "10504 WD-HSP-UK-GPBT-PYC(10).docx"
        ]
        # Delete records
        delete_records_by_filename(rds_credentials, table_name, filenames_to_delete)
