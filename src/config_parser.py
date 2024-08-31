import yaml
import sys


# Function reads & parses the YAML configuration file
def initial_yaml_read(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)  # Return parsed YAML content as a Python object

        if 'global_settings' not in config:
            config['global_settings'] = {}
        if 'port' not in config['global_settings']:
            config['global_settings']['port'] = 8989  # Default port if not specified
        if 'targets' not in config:
            raise KeyError("Missing 'targets' in configuration")

        return config
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f'Invalid YAML syntax: {e}')
    except FileNotFoundError:
        raise FileNotFoundError(f'YAML file not found: {file_path}')


# Only used when module ran independently
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


def main():
    # Get config file path
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = '../configs/app_db.yml'

    print(f"Using config file: {config_path}")

    try:
        config = initial_yaml_read(config_path) # Load config file

        # Detect the configuration type(s)
        config_types = detect_config_type(config)

        print("Detected configuration type(s):")
        for config_type in config_types:
            print(f"- {config_type}")

        print("\nTop-level keys:")
        for key in list(config.keys())[:3]:
            print(f"{key}: {config[key]}")

        print("Full configuration:", config)  # ?

        # Print the port configuration
        port = config['global_settings']['port']
        print(f"\nConfigured port: {port}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Error locating file, verify correct path.")
        sys.exit(1)

    except yaml.YAMLError as e:
        print(f"Error: {e}")
        print("Syntax error, verify YAML.")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    else:
        print("Configuration loaded and processed successfully")

    finally:
        # Executes at end regardless of whether an exception was raised
        print("Configuration processing complete")


if __name__ == "__main__":
    main()