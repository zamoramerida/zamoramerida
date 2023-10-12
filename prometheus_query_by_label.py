import requests
import yaml

# Replace with your Prometheus API URL
prometheus_url = 'http://your-prometheus-instance:9090'

# Function to execute a PromQL query and retrieve the results
def execute_query(promql_query):
    params = {'query': promql_query}
    response = requests.get(f'{prometheus_url}/api/v1/query', params=params)
    if response.status_code == 200:
        query_result = response.json()
        return query_result
    else:
        print(f'Failed to execute query: {promql_query}')
        return None

# Function to get distinct label values for a given label name
def get_label_values(label_name):
    response = requests.get(f'{prometheus_url}/api/v1/label/{label_name}/values')
    if response.status_code == 200:
        label_values = response.json()['data']
        return label_values
    else:
        print(f'Failed to fetch label values for {label_name}')
        return []

# Read the metrics definitions from the YAML file
with open('metrics.yml', 'r') as yaml_file:
    metrics_data = yaml.safe_load(yaml_file)

# List of label names for which you want to fetch values
label_names = ['tenants', 'communities']

# Create PromQL queries based on fetched label values and metric definitions
for label_name in label_names:
    label_values = get_label_values(label_name)
    if label_values:
        print(f'Label Name: {label_name}')
        for tenant, metrics_to_be_collected in metrics_data[label_name].items():
            print(f'Tenant: {tenant}')
            for metric_definition in metrics_to_be_collected:
                metric_name = metric_definition['metric']
                query = metric_definition['query']
                for value in label_values:
                    # Construct PromQL queries using the fetched label values
                    promql_query = f'{metric_name}{{{label_name}="{value}"}}'
                    final_query = query.replace('{{metric}}', promql_query)
                    print(f'PromQL Query for {metric_name}: {final_query}')

                    # Execute the query and retrieve the results
                    result = execute_query(final_query)
                    if result is not None:
                        print(f'Result for {metric_name} - {value}: {result}')
    else:
        print(f'No label values found for {label_name}')
