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
    <div className={style["status_div"]}>
      <div
        style={{
          marginRight: "0.25em",
          backgroundColor: colors[status],
          width: "0.5em",
          height: "0.5em",
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
  const [llmStatus, setLlmStatus] = useState<StatusTypes>("unknown");

  useEffect(() => {
    sio.on("connection", () => {
      setServerConnectionStatus("good");
    });

    sio.on("disconnect", () => {
      log("Client disconnected from server.", "warning");
      setServerConnectionStatus("bad");
      setModelSpeechRecognitionStatus("unknown");
      setModelSpeechGenerationStatus("unknown");
    });
  }, []);

  return (
    <Draggable>
      <div className={style["div"]}>
        <div>
          <StatusLog
            status={serverConnectionStatus}
            label="Server Connection Status"
            testFunction={() => {
              try {
                sio.emit("ping", null, () => {
                  setServerConnectionStatus("good");
                });
              } catch (error) {
                console.error(error);
                setServerConnectionStatus("bad");
              }
            }}
          />
          <StatusLog
            status={modelSpeechRecognitionStatus}
            label="Model Speech Recog. Status"
            testFunction={() => {
              try {
                sio.emit("model_test-audiorecog", null, (status: boolean) => {
                  setModelSpeechRecognitionStatus(status ? "good" : "bad");
                });
              } catch (error) {
                console.error(error);
                setModelSpeechRecognitionStatus("bad");
              }
            }}
          />
          <StatusLog
            status={modelSpeechGenerationStatus}
            label="Model Speech Gen. Status"
            testFunction={() => {
              try {
                sio.emit("model_test-audiogen", null, (status: boolean) => {
                  setModelSpeechGenerationStatus(status ? "good" : "bad");
                });
              } catch (error) {
                console.error(error);
                setModelSpeechGenerationStatus("bad");
              }
            }}
          />
          <StatusLog
            status={llmStatus}
            label="LLM Status"
            testFunction={() => {
              try {
                sio.emit("model_test-llm", null, (status: boolean) => {
                  setLlmStatus(status ? "good" : "bad");
                });
              } catch (error) {
                console.error(error);
                setLlmStatus("bad");
              }
            }}
          />
        </div>
      </div>
    </Draggable>
  );
}

export default StatusContainer;
