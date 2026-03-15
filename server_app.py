from flask import Flask, jsonify
import psutil
import socket
import threading
import time

app = Flask(__name__)

def cpu_load_task():
    """
    This function runs a loop for a fixed duration (e.g., 10 seconds)
    to keep the CPU busy.
    """
    print(f"[{socket.gethostname()}] Starting CPU load task...")
    start_time = time.time()
    # Run the intensive loop for 10 seconds
    while time.time() - start_time < 10:
        _ = [i*i for i in range(10**5)]
    print(f"[{socket.gethostname()}] CPU load task finished.")


@app.route('/')
def index():
    return f"<h1>Hello from Server: {socket.gethostname()}</h1>"

@app.route('/metrics')
def metrics():
    cpu_usage = psutil.cpu_percent(interval=0.1)
    return jsonify({'cpu_percent': cpu_usage})

@app.route('/load')
def load():
    # Create a new thread object that will run our cpu_load_task function
    load_thread = threading.Thread(target=cpu_load_task)
    load_thread.start()
    
    # Immediately return a response to the controller.
    # The server is NOT blocked and can continue to respond to /metrics requests.
    return "CPU load simulation started in the background."

if __name__ == '__main__':
    # Flask's development server is single-threaded by default.
    # We need to allow it to handle multiple requests at once.
    app.run(host='0.0.0.0', port=5000, threaded=True)