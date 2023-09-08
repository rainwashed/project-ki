import { io } from "socket.io-client";

const websocketServerLocation: string = "ws://localhost:4000";
const sio = io(websocketServerLocation, {
  autoConnect: false,
});

export { websocketServerLocation, sio };
