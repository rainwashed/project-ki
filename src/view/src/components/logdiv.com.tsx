import { useEffect, useState } from "react";
import { sio } from "../config";

function LogContainer() {
  const [logMessages, setLogMessages] = useState<string[]>([]);

  useEffect(() => {
    sio.on("log_event", (message) => {
      console.log(message);
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
        {logMessages.map((message, index) => (
          <li key={index}>
            <p>{message}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default LogContainer;
