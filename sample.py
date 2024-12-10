import boto3
import time
import os

# Initialize S3 client
s3 = boto3.client('s3')

# Configuration
bucket_name = "sb-udv3-tenant-06524939-tenantbucket-lownxjjywhf"
local_download_path = "response.json"  # Define the local file path for download
max_retries = 2  # Maximum number of retries
wait_time = 30  # Time to wait between retries (in seconds)

def check_and_download(file_path):
    # Extract filename from the S3 path
    filename = file_path.split("/")[-1]
    analysis_folder = f"{file_path}-analysis/"
    response_file_key = os.path.join(analysis_folder, "response.json")

    for attempt in range(max_retries + 1):
        try:
            # Check if the response.json exists
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=response_file_key)
            if "Contents" in response:
                print("response.json found! Downloading...")
                s3.download_file(bucket_name, response_file_key, local_download_path)
                print(f"File downloaded successfully to {local_download_path}")
                return
            else:
                print(f"Attempt {attempt + 1}: response.json not found. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        except Exception as e:
            print(f"An error occurred: {e}")

    print("response.json not found after multiple retries. Exiting...")

# Main function
if __name__ == "__main__":
    # Path extracted from the image
    file_path = "hiscox-policywording-xaas-dev/property_contents/5996 WD-PIP-UK-PYE(8)_sub.pdf"
    print(f"Checking for response.json in {file_path}-analysis...")
    check_and_download(file_path)
