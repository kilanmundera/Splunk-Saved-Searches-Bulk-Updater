# Splunk Saved Searches Bulk Updater

This Python script allows you to update parameters for multiple saved searches in a specific Splunk app. It provides the flexibility to update both simple key-value pairs and JSON dictionary parameters within saved searches. Additionally, it allows appending to existing JSON dictionary values without overwriting them.

## Features

- Update simple key-value pairs or JSON dictionary parameters.
- Append new values to existing JSON lists in dictionary-based parameters.
- Option to update all saved searches in an app or a single specific saved search.
- Secure password input.
  
## Requirements

- Python 3.x
- `splunklib` Python SDK (Install using `pip install splunk-sdk`)

## Installation

1. Install Python dependencies:
   ```bash
   pip install splunk-sdk
   ```
2. Clone the repository or copy the script to your working directory.

3. Run the script using Python 3.x.

## Usage

Run the script with the necessary command-line arguments to update the desired saved search parameters. Below are the available arguments and options.

### Arguments

| Argument       | Description                                                                                          | Required |
|----------------|------------------------------------------------------------------------------------------------------|----------|
| `--app`        | The name of the Splunk app where the saved searches are located.                                       | Yes      |
| `--parameter`  | The parameter to update (e.g., `action.correlationsearch.annotations`).                                | Yes      |
| `--value`      | The new value for the parameter. Multiple values can be specified when using `--json-dico`.            | Yes      |
| `--json-dico`  | If set, the parameter is treated as a JSON dictionary, requiring a `--key` argument.                   | Optional |
| `--key`        | The key to update within the JSON dictionary (required when using `--json-dico`).                      | Optional |
| `--append`     | If set, append the new value(s) to the existing list in the JSON dictionary rather than overwriting.   | Optional |
| `--search`     | Optionally update only the specified saved search by its name.                                         | Optional |
| `--host`       | The Splunk host (default: `localhost`).                                                               | Optional |
| `--port`       | The Splunk port (default: `8089`).                                                                    | Optional |
| `--username`   | The Splunk username (default: `admin`).                                                               | Optional |

### Password Prompt

The script prompts for the Splunk password via the terminal.

### Example Usage

1. **Updating a simple key=value pair**:
   ```bash
   python3 savedsearches_bulk_updater.py --app "my_app" --parameter "some_parameter" --value "new_value" --host "localhost" --username "admin"
   ```
   This updates the `some_parameter` in all saved searches within the app "my_app" to have the value `new_value`.

2. **Updating a JSON dictionary parameter**:
   ```bash
   python3 savedsearches_bulk_updater.py --app "my_app" --parameter "action.correlationsearch.annotations" --key "context" --value "PROD" --json-dico --host "localhost" --username "admin"
   ```
   This updates the JSON dictionary `action.correlationsearch.annotations` and set the value of `"context"` to `["PROD"]`.

3. **Appending to an existing JSON dictionary value**:
   ```bash
   python3 savedsearches_bulk_updater.py --app "my_app" --parameter "action.correlationsearch.annotations" --key "context" --value "PROD" --append --json-dico --host "localhost" --username "admin"
   ```
   If `"context"` already has the value `["DEV"]`, this appends `PROD` to it, resulting in `["DEV", "PROD"]`.

4. **Updating only one specific saved search**:
   ```bash
   python3 savedsearches_bulk_updater.py --app "my_app" --parameter "action.correlationsearch.annotations" --key "context" --value "DEV" --json-dico --search "my_saved_search" --host "localhost" --username "admin"
   ```
   This only updates the saved search named `my_saved_search`.

5. **Appending multiple values to an existing JSON key**:
   ```bash
   python3 savedsearches_bulk_updater.py --app "my_app" --parameter "action.correlationsearch.annotations" --key "context" --value "PROD" "STAGE" --append --json-dico --host "localhost" --username "admin"
   ```
   If `context` already has values `["DEV"]`, this appends `PROD` and `STAGE`, resulting in `["DEV", "PROD", "STAGE"]`.

### Error Handling

- If you set the `--json-dico` option, the `--key` argument is **required**.
- If the `--json-dico` option is **not** set, the `--key` argument should **not** be used.
- If an invalid combination of arguments is provided, the script will display an error and terminate.


## License

This project is licensed under the GPL-3.0 license.

## Support

For any questions or issues, feel free to open an issue in the repository or contact the author.
