import Draggable from "react-draggable";
import { sio } from "../config";
import style from "./styles/statusdiv.module.scss";
import { useEffect, useState } from "react";
import { log } from "./logdiv.com";

type StatusTypes = "good" | "bad" | "unknown";

function StatusLog({
  status,
  label,
  testFunction,
}: {
  status: StatusTypes;
  label: string;
  testFunction: VoidFunction;
}) {
  const colors = {
    good: "#00b894",
    bad: "#d63031",
    unknown: "#fdcb6e",
  };

  return (
    <div>
      <div
        style={{
          backgroundColor: colors[status],
          width: "0.25em",
          height: "0.25em",
          borderRadius: "50%",
        }}
      ></div>
      <span>{label}</span>
      <button onClick={testFunction}>Test</button>
    </div>
  );
}

function StatusContainer() {
  const [serverConnectionStatus, setServerConnectionStatus] =
    useState<StatusTypes>("unknown");
  const [modelSpeechRecognitionStatus, setModelSpeechRecognitionStatus] =
    useState<StatusTypes>("unknown");
  const [modelSpeechGenerationStatus, setModelSpeechGenerationStatus] =
    useState<StatusTypes>("unknown");

  useEffect(() => {
    sio.on("disconnect", () => {
      log("Client disconnected from server.", "warning");
      setServerConnectionStatus("bad");
    });
  }, []);

  return (
    <Draggable>
      <div className={style["div"]}>
        <div>
          <StatusLog
            status={serverConnectionStatus}
            label="Server Connection Status"
            testFunction={() => {}}
          />
          <StatusLog
            status={modelSpeechRecognitionStatus}
            label="Model Speech Recog. Status"
            testFunction={() => {}}
          />
          <StatusLog
            status={modelSpeechGenerationStatus}
            label="Model Speech Gen. Status"
            testFunction={() => {}}
          />
        </div>
      </div>
    </Draggable>
  );
}

export default StatusContainer;
