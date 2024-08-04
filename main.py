# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import config_parser
import ping_monitor


def main():
    # Load configuration
    config = config_parser.initial_yaml_read('./examples/targets.yaml')

    # Check if 'targets' is in the configuration
    if 'targets' not in config:
        print("Error: 'targets' not found in configuration")
        return

    # Ping each target
    for target in config['targets']:
        print(f"\nPinging {target}...")
        results = ping_monitor.ping_server(target)
        ping_monitor.display_ping_results(results)


if __name__ == "__main__":
    main()