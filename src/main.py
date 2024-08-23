import config_parser
import ping_monitor
import sys
import os
from prometheus_client import start_http_server
import time


def get_user_input(prompt, default=None):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default


def run_ping_monitor(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Config file '{config_path}' not found.")
        return

    try:
        config = config_parser.initial_yaml_read(config_path)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return

    if 'targets' not in config:
        print("Error: 'targets' not found in configuration")
        return

    global_settings = config.get('global_settings', {})
    probes = global_settings.get('probes', 4)
    interval = global_settings.get('interval', 1)

    while True:
        for target in config['targets']:
            print(f"\nPinging {target}...")
            results = ping_monitor.ping_server(
                target,
                count=probes,
                interval=interval
            )
            ping_monitor.display_and_expose_results(results, target)

        # Wait before the next round of pings
        time.sleep(60)  # Wait for 60 seconds before the next round


def main():
    # Start Prometheus HTTP server
    start_http_server(8989)
    print("Prometheus metrics server started on port 8989")

    # Get config file path
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = '../examples/variety.yml'

    print(f"Using config file: {config_path}")

    try:
        run_ping_monitor(config_path)
    except KeyboardInterrupt:
        print("\nPing monitor stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Ping monitor shutting down.")


if __name__ == "__main__":
    main()