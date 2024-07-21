import yaml
import sys

# Define the path to the YAML configuration file
config_path = 'examples/config.yaml'


# Define a function to read and parse the YAML configuration file
def initial_yaml_read(file_path):
    try:
        with open(file_path, 'r') as file:
            # Parse the YAML content and return it as a Python object
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f'Invalid YAML syntax: {e}')
    except FileNotFoundError:
        raise FileNotFoundError(f'YAML file not found: {file_path}')


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    try:
        # Attempt to load the configuration by calling the function
        config = initial_yaml_read(config_path)

        # Access the 'host' key nested under the 'database' key in the config
        database_host = config['database']['host']
        # Print the database host
        print(f"Database host: {database_host}")

        # Iterate over the 'users' list in the config
        for user in config['users']:
            # Print each user
            print(f"User: {user}")

        # Add more configuration usage as needed
        print("Full configuration:", config) #remove

    except FileNotFoundError as e:
        # Handle the case where the config file is not found
        print(f"Error: {e}")
        print("Error locating file, verify correct path.")
        sys.exit(1)

    except yaml.YAMLError as e:
        # Handle YAML syntax errors
        print(f"Error: {e}")
        print("Please check your YAML file for syntax errors.")
        sys.exit(1) # Exit the script with an error code

    except KeyError as e:
        # Handle missing keys in the configuration
        print(f"Error: Missing expected configuration key: {e}")
        print("Please ensure all required keys are present in the config file.")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    else:
        print("Configuration loaded and processed successfully")

    finally:
        # Executes at end regardless of whether an exception was raised
        print("Configuration processing complete")