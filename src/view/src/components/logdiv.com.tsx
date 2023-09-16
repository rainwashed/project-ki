import { useEffect, useState } from "react";
import { sio } from "../config";

// TODO: Fix socket.io emit calling twice for some reason

function LogContainer() {
  const [logMessages, setLogMessages] = useState<string[]>([]);

  useEffect(() => {
    sio.on("log_message", (message) => {
      console.log(logMessages);

      setLogMessages([...logMessages, message]);
    });
  }, [logMessages]);

  return (
    <div
      style={{
        backgroundColor: "red",
      }}
    >
      <ul>
        {logMessages.slice().map((message, i) => (
          <li key={i}>
            <p>{message}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default LogContainer;
