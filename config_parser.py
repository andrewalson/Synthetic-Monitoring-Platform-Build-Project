import yaml
import sys


config_path = 'examples/app_db.yml'


# Function reads & parses the YAML configuration file
def initial_yaml_read(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)  # Return parsed YAML content as a Python object
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f'Invalid YAML syntax: {e}')
    except FileNotFoundError:
        raise FileNotFoundError(f'YAML file not found: {file_path}')


def detect_config_type(config):
    type_indicators = {
        'Application': ['app', 'name', 'version'],
        'Server': ['server', 'host', 'port'],
        'Database': ['database', 'host', 'name'],
        'Logging': ['logging', 'level', 'file'],
        'Cache': ['cache', 'type', 'host'],
        'API': ['api', 'version', 'rate_limit'],
        'Security': ['security', 'secret_key', 'allowed_hosts'],
        'Email': ['email', 'smtp_server', 'username'],
        'Feature Flags': ['features'],
        'External Services': ['services']
    }

    detected_types = []

    # Check for each type
    for config_type, indicators in type_indicators.items():
        if any(indicator in config for indicator in indicators):
            detected_types.append(config_type)

    return detected_types if detected_types else ['Unknown']


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    try:
        config = initial_yaml_read(config_path) # Load config file

        # Detect the configuration type(s)
        config_types = detect_config_type(config)

        print("Detected configuration type(s):")
        for config_type in config_types:
            print(f"- {config_type}")

        print("\nTop-level keys::")
        for key in list(config.keys())[:3]:
            print(f"{key}: {config[key]}")

        # # Iterate over the 'users' list in the config
        # for user in config['users']:
        #     # Print each user
        #     print(f"User: {user}")

        print("Full configuration:", config)  # ?

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Error locating file, verify correct path.")
        sys.exit(1)

    except yaml.YAMLError as e:
        print(f"Error: {e}")
        print("Syntax error, verify YAML.")
        sys.exit(1)

    # except KeyError as e:
    #     print(f"Error: Missing expected configuration key: {e}")
    #     print("Please ensure all required keys are present in the config file.")
    #     sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    else:
        print("Configuration loaded and processed successfully")

    finally:
        # Executes at end regardless of whether an exception was raised
        print("Configuration processing complete")
