import config_parser
import ping_monitor
import sys
import os
from prometheus_client import start_http_server
import time
import threading
import queue

# Add this near the top of the file, after the imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'configs', 'variety.yml')

# def get_user_input(prompt, default=None):
#     value = input(f"{prompt} [{default}]: ").strip()
#     return value if value else default


def run_ping_monitor(config_path, output_queue=None):
    if not os.path.exists(config_path):
        message = f"Error: Config file '{config_path}' not found."
        output(message, output_queue)
        return

    try:
        config = config_parser.initial_yaml_read(config_path)
    except Exception as e:
        message = f"Error loading config file: {e}"
        output(message, output_queue)
        return

    global_settings = config.get('global_settings', {})
    probes = global_settings.get('probes', 4)
    interval = global_settings.get('interval', 1)
    port = global_settings.get('port', 8989)

    # Start Prometheus HTTP server
    start_http_server(port)
    message = f"Prometheus metrics server started on port {port}"
    output(message, output_queue)

    while True:
        for target in config['targets']:
            message = f"\nPinging {target}..."
            output(message, output_queue)
            results = ping_monitor.ping_server(
                target,
                count=probes,
                interval=interval
            )
            ping_monitor.display_and_expose_results(results, target)
            output(str(results), output_queue)

        # Wait before the next round of pings
        time.sleep(60)  # Wait for 60 seconds before the next round

def output(message, queue=None):
    if queue:
        queue.put(message)
    else:
        print(message)

def start_monitor_thread(config_path, output_queue):
    thread = threading.Thread(target=run_ping_monitor, args=(config_path, output_queue))
    thread.daemon = True
    thread.start()
    return thread

def main():
    # Get config file path
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = DEFAULT_CONFIG_PATH

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