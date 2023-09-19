import requests
import boto3
from botocore.auth import SigV4Auth

# Configure AWS credentials from your AWS CLI configuration
aws_session = boto3.Session()

# Define the AMP query endpoint URL
amp_query_url = "https://aps-workspaces.<your-region>.amazonaws.com/workspaces/<workspace-id>/query"

# Define the AWS region and service for AWS Signature Version 4
aws_region = "<your-aws-region>"
aws_service = "aps"

# Define your AMP query
amp_query = "your_prometheus_query_here"

# Create a session with the AWS Signature Version 4 authentication handler
session = requests.Session()

# Send a POST request to the AMP query endpoint
try:
    headers = {
        "Content-Type": "application/json",
        "X-Amz-Target": "AmazonPrometheus.GraphQL.ExecuteQuery",
    }
    data = {
        "query": amp_query,
    }

    request = requests.Request('POST', amp_query_url, json=data, headers=headers)
    prepared_request = session.prepare_request(request)

    # Sign the request using AWS Signature Version 4
    auth = SigV4Auth(aws_session.get_credentials(), aws_service, aws_region)
    auth.add_auth(prepared_request)

    response = session.send(prepared_request)
    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()
    # Handle the response data here

    print("AMP Query Endpoint is reachable!")

except requests.exceptions.RequestException as e:
    print(f"Failed to reach AMP Query Endpoint: {e}")

# Process the result from the AMP query response
if "data" in result:
    # Extract and process the data as needed
    query_result = result["data"]["executePromQL"]["result"]

    # Add your logic to work with the query_result data
