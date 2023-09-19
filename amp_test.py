import requests
import boto3
from botocore.auth import SigV4Auth
import botocore.session
from botocore.awsrequest import AWSRequest


# Configure AWS credentials from your AWS CLI configuration
aws_session = boto3.Session()

# Define the AMP query endpoint URL
amp_query_url = "https://aps-workspaces.<your-region>.amazonaws.com/workspaces/<workspace-id>/query"

# Define the AWS region and service for AWS Signature Version 4
aws_region = "<your-aws-region>"
aws_service = "aps"

# Define your AMP query
amp_query = "your_prometheus_query_here"
sigv4 = SigV4Auth(aws_session.get_credentials(), aws_service, aws_region)

# Create a session with the AWS Signature Version 4 authentication handler
session = botocore.session.Session()

# Send a POST request to the AMP query endpoint
try:
    headers = {
        "Content-Type": "application/json",
        "X-Amz-Target": "AmazonPrometheus.GraphQL.ExecuteQuery",
    }
    data = {
        "query": amp_query,
    }

    #request = requests.Request('POST', amp_query_url, json=data, headers=headers)
													   

    request = AWSRequest(method='POST', url=amp_query_url, data=data, headers=headers)
    request.context["payload_signing_enabled"] = False # payload signing is not supported
    sigv4.add_auth(request)
    
    prepped = request.prepare()


    response = requests.post(prepped.url, headers=prepped.headers, data=data)

    # Sign the request using AWS Signature Version 4

    result = response.json()
    # Handle the response data here

    print("AMP Query Endpoint is reachable!")

except requests.exceptions.RequestException as e:
    print(f"Failed to reach AMP Query Endpoint: {e}")
