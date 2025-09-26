Swarm Operator Package
======================

Contents:
- index.html            : Single-file operator web app (map, drone list, auto-assign, mission)
- server.js             : Node.js backend (WebSocket + REST)
- esp32_client.ino      : Example ESP32 WebSocket client (Arduino) to simulate drone
- README.md             : This file

How to use (quickstart)
-----------------------
1) Run backend (optional - the web app has simulation mode)
   - Requirements: Node.js (v14+)
   - Install:
       npm install express ws body-parser uuid
   - Start:
       node server.js
   - Backend runs on http://localhost:8080 and ws://localhost:8080 by default.

2) Open the operator web app
   - Open index.html in a browser (Chrome recommended).
   - Login (demo) and toggle 'Simulate Drones' (checked) to demo without server.
   - To connect to backend, uncheck 'Simulate Drones', set REST and WS URLs, click Connect.

3) Use the map:
   - Click to add waypoints. Edit altitude in the left panel.
   - Click 'Auto-Assign' to assign drones to waypoints.
   - Click 'Start Mission' to POST /mission to backend (or simulate).

4) ESP32 client (demo)
   - Edit esp32_client.ino: set WiFi SSID/password and ws_server IP.
   - Install ArduinoJson and arduinoWebSockets libraries.
   - Upload to ESP32; it will JOIN and send HEARTBEAT messages to the backend.

Security & production notes
---------------------------
- This package is a demo. For production:
  - Use TLS (wss://) and authentication (JWT, OAuth).
  - Implement HMAC/AES for message integrity and encryption.
  - Harden backend with rate limiting and authentication.

Files location:
- /mnt/data/swarm_operator_package/

Download
--------
A zip with all files is prepared alongside this README.

