import requests

# Replace with your Prometheus API URL
prometheus_url = 'http://your-prometheus-instance:9090'

# Function to get distinct label values for a given label name
def get_label_values(label_name):
    response = requests.get(f'{prometheus_url}/api/v1/label/{label_name}/values')
    if response.status_code == 200:
        label_values = response.json()['data']
        return label_values
    else:
        print(f'Failed to fetch label values for {label_name}')
        return []

# List of label names for which you want to fetch values
label_names = ['tenants', 'communities']

# Create PromQL queries based on fetched label values
for label_name in label_names:
    label_values = get_label_values(label_name)
    if label_values:
        print(f'Label Name: {label_name}')
        for value in label_values:
            # Create PromQL queries using the fetched label values
            promql_query = f'{label_name}="{value}"'
            print(f'PromQL Query: {promql_query}')
    else:
        print(f'No label values found for {label_name}')
