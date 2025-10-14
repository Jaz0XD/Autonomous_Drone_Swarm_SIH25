from flask import Flask, render_template, Response, request, jsonify
import cv2

app = Flask(__name__)  # ✅ FIXED (_name_ → __name__)

# ✅ Corrected IPs (must have proper formatting)
camera_urls = {
    1: "http://192.168.172.86:8080/video",#thiyagu
    2: "http://192.168.172.137:8080/video",#siraj
    3: "http://192.168.172.168:8080/video",#prag
}

# ✅ Generate video frames for streaming
def generate_frames(url):
    cap = cv2.VideoCapture(url)
    while True:
        success, frame = cap.read()
        if not success:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ✅ Home route
@app.route('/')
def index():
    return render_template('index.html')  # Ensure 'index.html' is in 'templates' folder

# ✅ Video stream route
@app.route('/video/<int:cam_id>')
def video(cam_id):
    if cam_id in camera_urls:
        return Response(generate_frames(camera_urls[cam_id]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Camera not found", 404

# ✅ Initial drone coordinates
drone_locations = {
    1: {"id": 1, "lat": 12.9716, "lon": 77.5946},  # Bangalore
    2: {"id": 2, "lat": 13.0827, "lon": 80.2707},  # Chennai
    3: {"id": 3, "lat": 11.0168, "lon": 76.9558},  # Coimbatore
    4: {"id": 4, "lat": 9.9252, "lon": 78.1198}    # Madurai
}

# ✅ Fetch all drone locations
@app.route('/locations')
def get_locations():
    return jsonify({"drones": list(drone_locations.values())})

# ✅ Update drone location (when user clicks map)
@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    drone_id = data.get('id')
    lat = data.get('lat')
    lon = data.get('lon')

    if drone_id in drone_locations:
        drone_locations[drone_id]['lat'] = lat
        drone_locations[drone_id]['lon'] = lon
        print(f"📍 Updated Drone {drone_id} → ({lat}, {lon})")
        return jsonify({"status": "updated", "drone_id": drone_id})
    return jsonify({"error": "Drone not found"}), 404

# ✅ Command control (takeoff, land, etc.)
@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    action = data.get('action')
    print(f"🚁 Drone command received: {action}")
    # You can integrate with actual drone control APIs here.
    return jsonify({"status": "ok", "action": action})

# ✅ Correct main entry
if __name__ == "__main__":  # FIXED
    app.run(host="0.0.0.0", port=5000, debug=True)
