'''
This module provides the optional Flask-based web interface.
Run with 'python frontend.py' or 'flask --app frontend run'

Global Variables:
    app (Flask): The Flask application instance
    output_queue (Queue): Queue for storing monitoring output messages
    persistent_messages (list): List for storing recent messages
    monitor_thread (Thread): Thread running the monitoring process
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import sys
import queue
import threading

# Add parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import start_monitor_thread, DEFAULT_CONFIG_PATH

app = Flask(__name__)

output_queue = queue.Queue()
monitor_thread = None
persistent_messages = []

def message_processor():
    while True:
        message = output_queue.get()
        persistent_messages.append(message)
        if len(persistent_messages) > 1000:
            persistent_messages.pop(0)

# Start message processor thread
processor_thread = threading.Thread(target=message_processor, daemon=True)
processor_thread.start()

@app.route('/')
def index():
    return render_template('index.html', default_config_path=DEFAULT_CONFIG_PATH)

@app.route('/set_config', methods=['POST'])
def set_config():
    '''
    Called when user submits config path via form on index page.
    Starts or restarts the monitor thread with specified configuration.
    Returns rendered HTML content of index page with status message.
    '''
    global monitor_thread
    config_path = request.form['config_path']
    if not config_path:
        config_path = DEFAULT_CONFIG_PATH
    
    if os.path.exists(config_path):
        # Stop the existing monitor thread if it's running
        if monitor_thread:
            # TODO: proper shutdown mechanism
            pass
        
        # Clear previous messages
        persistent_messages.clear()
        
        # Start a new monitor thread
        monitor_thread = start_monitor_thread(config_path, output_queue)
        message = f"Config set and monitor started with: {config_path}"
    else:
        message = f"Error: Config file not found at {config_path}"
    
    persistent_messages.append(message)
    return render_template('index.html', message=message, default_config_path=DEFAULT_CONFIG_PATH)

@app.route('/output')
def output():
    '''
    Retrieves messages from output queue & displays them on the output page.
    '''
    messages = []
    while not output_queue.empty():
        messages.append(output_queue.get())
    return render_template('output.html', messages=persistent_messages)

if __name__ == '__main__':
    app.run(debug=True)