import { useTrafficStore } from '../store/trafficStore';

// Assuming local testing for MVP. Change IP if testing on physical device.
const WS_URL = 'ws://127.0.0.1:8000/ws/traffic'; 

let ws: WebSocket | null = null;
let reconnectInterval: NodeJS.Timeout;

export const connectWebSocket = () => {
  if (ws) return;

  try {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log('Connected to VAZHI-AI WebSocket');
      useTrafficStore.getState().setConnected(true);
      if (reconnectInterval) clearInterval(reconnectInterval);
    };

    ws.onmessage = (e) => {
      if (e.data === 'pong') return;
      try {
        const data = JSON.parse(e.data);
        useTrafficStore.getState().updateState(data);
      } catch (err) {
        console.error('Error parsing WS data:', err);
      }
    };

    ws.onclose = () => {
      console.log('Disconnected from VAZHI-AI WebSocket');
      useTrafficStore.getState().setConnected(false);
      ws = null;
      reconnectInterval = setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (e) => {
      console.error('WebSocket Error:', e);
      ws?.close();
    };
  } catch (error) {
    console.error('WebSocket connection failed', error);
  }
};

export const disconnectWebSocket = () => {
  if (ws) {
    ws.close();
    ws = null;
  }
};
