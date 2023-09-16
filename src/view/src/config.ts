import { extendTheme } from "@chakra-ui/react";
import { io } from "socket.io-client";

const websocketServerLocation: string = "ws://localhost:4000";
const sio = io(websocketServerLocation, {
  autoConnect: false,
});

const customTheme = extendTheme({});

export { websocketServerLocation, sio, customTheme };
