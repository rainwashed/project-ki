import { useEffect, useState } from "react";
import { sio } from "../config";

// TODO: Fix socket.io emit calling twice for some reason

function LogContainer() {
  const [logMessages, setLogMessages] = useState<string[]>([]);

  useEffect(() => {
    sio.on("log_message", (message) => {
      setLogMessages([...logMessages, message]);
    });
  }, []);

  return (
    <div
      style={{
        backgroundColor: "red",
      }}
    >
      <ul>
        {logMessages.map((message, i) => {
          return (
            <li key={i}>
              <p>{message}</p>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default LogContainer;
