import config_parser
import ping_monitor
import sys
import os
from prometheus_client import start_http_server
import time
import threading
import queue
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'configs', 'variety.yml')

def run_ping_monitor(config_path, output_queue=None):
    '''
    This function reads the configuration file, starts the Prometheus HTTP server,
    and continuously pings the specified targets, updating metrics & outputting results.

    Args:
        config_path (str): The path to the YAML configuration file.
        output_queue (queue.Queue, optional): Output messages queue for frontend. 
                                            If None, output is printed to console.
    '''
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
    probes = global_settings.get('probes', 5)
    interval = global_settings.get('interval', 1)
    port = global_settings.get('port', 8989)

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
            formatted_results = ping_monitor.display_and_expose_results(results, target)
            output(formatted_results, output_queue)

        # Wait 15 seconds before the next round of pings
        output("\nBatch complete. Starting new batch in 15 seconds...", output_queue)
        time.sleep(15)

def output(message, queue=None):
    '''
    Output a message either to a queue or to the console.

    Args:
        message (str): The message to output.
        queue (queue.Queue, optional): If provided, the message is put into this queue.
                                       If None, the message is printed to the console.
    '''
    # Remove the first line if it's blank
    message = re.sub(r'^\s*\n', '', message)
    
    if queue:
        queue.put(message)
    else:
        print(message)

def start_monitor_thread(config_path, output_queue):
    '''
    *** For now, only used when ran from frontend entry point ***

    This function creates and starts a new daemon thread that runs the ping monitor
    with the specified configuration.

    Args:
        config_path (str): The path to the YAML configuration file.
        output_queue (queue.Queue): A queue to store output messages from the monitor.
    Returns:
        threading.Thread: The started thread object.
    '''
    thread = threading.Thread(target=run_ping_monitor, args=(config_path, output_queue))
    thread.daemon = True
    thread.start()
    return thread

def main():
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