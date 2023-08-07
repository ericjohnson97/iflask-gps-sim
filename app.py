from flask import Flask, render_template, request, jsonify
import json
import subprocess
import time
import threading

app = Flask(__name__)

# Global variables
simulation_running = False
current_thread = None
current_position = (None, None)

def simulate_location(lat, lon):
    cmd = ["python3", "-m", "pymobiledevice3", "developer", "simulate-location", "set", "--", str(lat), str(lon)]
    print(cmd)
    subprocess.run(cmd)

def simulate_waypoints_from_file():
    global simulation_running
    global current_position
    with open('waypoints.json', 'r') as f:
        waypoints = json.load(f)
    
    for point in waypoints:
        if not simulation_running:  # Check the flag before simulating each location.
            break

        simulate_location(point['lat'], point['lng'])
        current_position = (point['lat'], point['lng'])
        time.sleep(1)  # Add delay if needed

    while simulation_running:

        # keep sending the last location
        simulate_location(waypoints[-1]['lat'], waypoints[-1]['lng'])

        # Keep the thread alive until the simulation is stopped.
        time.sleep(1)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/save-waypoints', methods=['POST'])
def save_waypoints():
    global simulation_running, current_thread

    if simulation_running:  # Prevent starting a new thread if one is already running.
        return jsonify({"message": "Simulation is already running!"})

    data = request.json
    waypoints = data.get('waypoints', [])
    
    with open('waypoints.json', 'w') as f:
        json.dump(waypoints, f)

    # Start the simulation in a separate thread.
    simulation_running = True
    current_thread = threading.Thread(target=simulate_waypoints_from_file)
    current_thread.start()

    return jsonify({"message": "Waypoints received and simulation started!"})

@app.route('/stop', methods=['POST'])
def stop_simulation():
    global simulation_running
    simulation_running = False

    # If you want to ensure that the thread finishes before proceeding, uncomment the next line.
    # current_thread.join()

    return jsonify({"message": "Simulation stopped!"})

@app.route('/get-current-position', methods=['GET'])
def get_current_position():
    global current_position
    lat, lon = current_position
    return jsonify({"lat": lat, "lon": lon})

@app.route('/get-waypoints', methods=['GET'])
def get_waypoints():
    try:
        with open('waypoints.json', 'r') as f:
            waypoints = json.load(f)
        return jsonify(waypoints)
    except FileNotFoundError:
        return jsonify([])



if __name__ == '__main__':
    app.run(debug=True)
