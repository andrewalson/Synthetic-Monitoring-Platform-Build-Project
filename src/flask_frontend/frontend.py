from flask import Flask, render_template, request, redirect, url_for
import os
import sys
import queue

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import start_monitor_thread, DEFAULT_CONFIG_PATH

app = Flask(__name__)

output_queue = queue.Queue()
monitor_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_config', methods=['POST'])
def set_config():
    global monitor_thread
    config_path = request.form['config_path']
    if not config_path:
        config_path = DEFAULT_CONFIG_PATH
    
    if os.path.exists(config_path):
        # Stop the existing monitor thread if it's running
        if monitor_thread:
            # You might want to implement a proper shutdown mechanism
            pass
        
        # Start a new monitor thread
        monitor_thread = start_monitor_thread(config_path, output_queue)
        message = f"Config set and monitor started with: {config_path}"
    else:
        message = f"Error: Config file not found at {config_path}"
    
    return render_template('index.html', message=message)

@app.route('/output')
def output():
    messages = []
    while not output_queue.empty():
        messages.append(output_queue.get())
    return render_template('output.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)