# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import config_parser
import ping_monitor
import sys
import os


def get_user_input(prompt, default=None):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default


def main():
    # Load configuration
    # Check for config file path is provided via command-line argument, else use hardcoded
    # Ex. 'python3 src/main.py examples/targets_probes_intervals.yaml' *python3*
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = './examples/targets_probes_intervals.yaml'

    # Check if the file exists
    if not os.path.exists(config_path):
        print(f"Error: Config file '{config_path}' not found.")
        return

    # Load (confirmed) existing configuration
    try:
        config = config_parser.initial_yaml_read(config_path)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return

    # Check if 'targets' is in the configuration
    if 'targets' not in config:
        print("Error: 'targets' not found in configuration")
        return

    # Get global settings or prompt user
    global_settings = config.get('global_settings', {})
    probes = global_settings.get('probes')
    if probes is None:
        probes = int(get_user_input("Enter number of probes", "4"))

    interval = global_settings.get('interval')
    if interval is None:
        interval = float(get_user_input("Enter interval between probes (in seconds)", "1"))

    # Ping each target
    for target in config['targets']:
        print(f"\nPinging {target['address']}...")
        results = ping_monitor.ping_server(
            target['address'],
            count=probes,
            interval=interval
        )
        ping_monitor.display_ping_results(results)


if __name__ == "__main__":
    main()