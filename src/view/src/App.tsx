import { useEffect, useState } from "react";
import { sio } from "./config";
import LogContainer, { log } from "./components/logdiv.com";

import "./styles/root.scss";
import StatusContainer from "./components/statusdiv.com";

function SendMessage() {
  const [input, setInput] = useState("");

  return (
    <div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      ></input>
      <button
        onClick={() => {
          log(input, "info");
          setInput("");
        }}
      >
        Send
      </button>
    </div>
  );
}

function App() {
  useEffect(() => {
    sio.connect();

    log(
      "Loaded all modules; if this message is visible, successful server connection.",
      "success"
    );

    return () => {
      sio.disconnect();
    };
  }, []);

  return (
    <div>
      <button
        onClick={() => {
          sio.emit(
            "model_test",
            {
              model: "audio_model",
            },
            (response: any) => {
              console.log(response);
            }
          );
        }}
      >
        Model Test
      </button>
      <div>
        <StatusContainer />
        <LogContainer />
      </div>

      <SendMessage />
    </div>
  );
}

function Wrapper() {
  return (
    <>
      <App />
    </>
  );
}

export default Wrapper;
