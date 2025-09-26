// server.js - simple backend for Swarm Operator Console
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(bodyParser.json());
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const drones = {}; // id -> { ws, lastSeen, pos, battery, state }

wss.on('connection', (ws, req) => {
  console.log('WS connection');
  ws.on('message', msg => {
    try {
      const data = JSON.parse(msg);
      if (data.type === 'JOIN_REQ') {
        const id = data.id || uuidv4();
        ws.droneId = id;
        drones[id] = { ws, lastSeen: Date.now(), pos:null, battery: null, state: 'CONNECTED', role: null };
        ws.send(JSON.stringify({ type: 'JOIN_RESP', status:'OK', id }));
        console.log('Drone joined', id);
      } else if (data.type === 'HEARTBEAT') {
        const id = data.id;
        if (drones[id]) {
          drones[id].lastSeen = Date.now();
          drones[id].pos = data.pos;
          drones[id].battery = data.battery;
          drones[id].state = data.state;
        }
      } else if (data.type === 'ACK') {
        console.log('ACK from', data.id, data.cmd_id);
      } else {
        // generic handling
        console.log('WS message', data);
      }
    } catch(e) { console.error('bad msg', e); }
  });

  ws.on('close', () => {
    const id = ws.droneId;
    if (id && drones[id]) {
      console.log('Drone disconnected', id);
      delete drones[id];
    }
  });
});

// REST API to list drones
app.get('/drones', (req, res) => {
  const list = Object.keys(drones).map(id => ({ id, lastSeen: drones[id].lastSeen, pos: drones[id].pos, battery: drones[id].battery, role: drones[id].role }));
  res.json(list);
});

// Create mission: assign waypoints and roles
app.post('/mission', (req, res) => {
  const { waypoints, assignments } = req.body; // assignments: [{droneId, waypointIndex, role, alt}]
  // send to drones
  assignments.forEach(a => {
    const d = drones[a.droneId];
    if (d && d.ws && d.ws.readyState === WebSocket.OPEN) {
      const cmd = { type:'ASSIGN_WAYPOINTS', cmd_id: uuidv4(), waypoints:[ waypoints[a.waypointIndex] ], role: a.role };
      d.ws.send(JSON.stringify(cmd));
    }
  });
  res.json({ status:'ok' });
});

server.listen(8080, () => console.log('Server running on :8080'));
