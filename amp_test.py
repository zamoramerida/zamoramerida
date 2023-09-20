import requests
from requests_aws4auth import AWS4Auth
import boto3

# Define the AWS region, profile, and query endpoint URL
aws_region = "region"
aws_profile = "saml"
query_endpoint = "https://aps-workspaces.region.amazonaws.com/workspaces/ws-XXXXXXXXX/api/v1/query"  # Replace with the actual endpoint
service_name = "aps"  # This should match the service you are using

# Create a session using your AWS profile
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

# Generate AWS Signature Version 4 credentials
credentials = session.get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key
token = credentials.token

# Construct the full URL with the query parameter
query_url = f"{query_endpoint}?query=up"

# Create the AWS4Auth object
auth = AWS4Auth(
    access_key,
    secret_key,
    aws_region,
    service_name,
    session_token=token,
)

# Make an HTTP POST request using the requests library and AWS Signature
headers = {
    "x-amz-security-token": token,
}

response = requests.post(query_url, headers=headers, auth=auth)

# Print the response
print("Response Status Code:", response.status_code)
print("Response Content:", response.text)
