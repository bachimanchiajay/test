import boto3
import os
import json

def process_image(file_path):
    print(f"Processing file: {os.path.basename(file_path)}")
    
    # Create the S3 client
    s3_client = boto3.client('s3', region_name='eu-west-2')

    # Clean and construct paths
    filename = os.path.basename(file_path).replace("_sub", "")
    analysis_folder = f"{os.path.dirname(file_path)}-analysis"
    response_file_key = os.path.join(analysis_folder, "response.json").replace("\\", "/")  # Ensure correct path formatting for S3
    bucket_name = 'sb-udv3-tenant-06524939-tenantbucket-lownxjjyrwhf'

    print(f"response file key --> {response_file_key}")
    print(f"bucket_name --> {bucket_name}")

    # Set the local download path
    local_download_path = "/app/response.json"
    os.makedirs(os.path.dirname(local_download_path), exist_ok=True)  # Create the directory if it doesn't exist

    try:
        # Download the file from S3
        s3_client.download_file(bucket_name, response_file_key, local_download_path)
        print(f"File downloaded successfully to {local_download_path}")

        # Load the file content
        with open(local_download_path, 'r') as file:
            response = json.load(file)
        
        # Process the response
        text = ""
        for item in response['Blocks']:
            if item['BlockType'] == "LINE":
                text += item['Text'] + "\n"

        print("Extracted Text:")
        print(text)
    except Exception as e:
        print(f"Error: {e}")
