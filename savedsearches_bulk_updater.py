import splunklib.client as client
import json
import argparse
import getpass
import sys

# Function to connect to Splunk
def connect_to_splunk(host, port, username, password):
    return client.connect(
        host=host,
        port=port,
        username=username,
        password=password
    )

# Function to determine if the value is JSON or not
def is_json(value):
    try:
        json.loads(value)
        return True
    except ValueError:
        return False

# Function to update saved searches
def update_saved_searches(service, app_name, parameter, value, json_dico, key=None, append=False, search_name=None):
    # Get the saved searches within the app
    savedsearches = service.saved_searches

    # Handle json-dico option: If set, we expect a key and the value will be handled as JSON
    if json_dico and key is None:
        print("Error: --key argument is required when --json-dico is set.")
        sys.exit(1)

    if not json_dico and key is not None:
        print("Error: --key argument should not be used when --json-dico is not set.")
        sys.exit(1)

    # If --json-dico is set and the key is provided, the value remains as a list
    if json_dico:
        if isinstance(value, str):  # Handle single value edge case
            value = [value]

    # Iterate over all saved searches
    for savedsearch in savedsearches:
        if savedsearch.access.app == app_name and (search_name is None or savedsearch.name == search_name):
            print(f"Processing saved search: {savedsearch.name}")

            if json_dico:
                # Get the current value of the parameter (JSON-like string)
                annotations = savedsearch.content.get(parameter, '{}')

                if is_json(annotations):
                    annotations_dict = json.loads(annotations)
                    
                    # Check if the key already exists in the dictionary
                    if key in annotations_dict:
                        if append:
                            # If we need to append the value to an existing key
                            print(f"Appending values {value} to existing key {key} in {savedsearch.name}")
                            if isinstance(annotations_dict[key], list):
                                annotations_dict[key].extend(value)  # Append the new values to the existing list
                            else:
                                annotations_dict[key] = [annotations_dict[key]] + value  # Convert to list and append
                        else:
                            print(f"Updating {key} in {savedsearch.name} with new value: {value}")
                            annotations_dict[key] = value  # Replace the value
                    else:
                        # If the key doesn't exist, add the new key-value pair
                        print(f"Adding new key {key} with value {value} to {savedsearch.name}")
                        annotations_dict[key] = value
                else:
                    annotations_dict = {key: value}

                # Convert the updated dictionary back to a JSON-like string
                updated_annotations = json.dumps(annotations_dict)

                # Update the saved search with the new annotations
                savedsearch.update(**{parameter: updated_annotations})

            else:
                # If json-dico is not set, treat the parameter as key=value pair
                print(f"Updating {parameter} in {savedsearch.name} with simple value: {value}")
                savedsearch.update(**{parameter: value})

            # Refresh to apply changes
            savedsearch.refresh()

    print("Completed updating saved searches.")

if __name__ == "__main__":
    # Argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Update saved searches in a Splunk app.")
    parser.add_argument('--app', required=True, help="The name of the Splunk app.")
    parser.add_argument('--parameter', required=True, help="The parameter to update (e.g., 'action.correlationsearch.annotations').")
    parser.add_argument('--value', nargs='+', required=True, help="The new value for the parameter (multiple values allowed if --json-dico is set).")
    parser.add_argument('--json-dico', action='store_true', help="If true, treat the parameter as a JSON dictionary and expect a --key argument.")
    parser.add_argument('--key', help="The key to update within the JSON dictionary (required if --json-dico is true).")
    parser.add_argument('--append', action='store_true', help="If true, append the new value to the existing value for the key (only works with --json-dico).")
    parser.add_argument('--search', help="Optional: Update only the specified saved search.")
    parser.add_argument('--host', default="localhost", help="The Splunk host.")
    parser.add_argument('--port', type=int, default=8089, help="The Splunk port.")
    parser.add_argument('--username', default="admin", help="The Splunk username.")

    # Parse the arguments
    args = parser.parse_args()

    # Check for argument consistency
    if args.json_dico and args.key is None:
        print("Error: --key is required when --json-dico is set.")
        sys.exit(1)
    if not args.json_dico and args.key is not None:
        print("Error: --key should not be used when --json-dico is not set.")
        sys.exit(1)

    # Prompt for the password securely
    password = getpass.getpass(prompt="Enter Splunk password: ")

    # Connect to Splunk
    service = connect_to_splunk(args.host, args.port, args.username, password)

    # Update the saved searches
    update_saved_searches(service, args.app, args.parameter, args.value, args.json_dico, args.key, args.append, args.search)

