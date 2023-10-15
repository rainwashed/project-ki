import { useEffect, useState } from "react";
import Draggable from "react-draggable";
import { sio } from "../config";

import style from "./styles/logdiv.module.scss";

// TODO: Implement client-side logging

function log(
  message: string,
  level: "info" | "warning" | "success" | "unknown" = "info"
) {
  const icon = {
    info: "ℹ️",
    warning: "⚠️",
    success: "✅",
    unknown: "❓",
  }[level];

  sio.emit("log", `[${Date.now()}, ${icon}] - ${message} (local)`);
}

function LogContainer() {
  const [logMessages, setLogMessages] = useState<string[]>([]);

  useEffect(() => {
    sio.on("log_message", (message) => {
      setLogMessages([...logMessages, message]);
    });
  }, [logMessages]);

  return (
    <Draggable>
      <div className={style["div"]}>
        {logMessages.length > 0 ? (
          <ul>
            {logMessages.slice().map((m, i) => {
              return <li key={i}>{m}</li>;
            })}
          </ul>
        ) : (
          <p>No logs yet...</p>
        )}
      </div>
    </Draggable>
  );
}

export default LogContainer;

// eslint-disable-next-line react-refresh/only-export-components
export { log };
