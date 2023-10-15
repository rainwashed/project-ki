import { useEffect, useState } from "react";
import { sio } from "./config";
import LogContainer, { log } from "./components/logdiv.com";

import "./styles/root.scss";
import StatusContainer from "./components/statusdiv.com";
import FunctionContainer from "./components/functiondiv.com";

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
      <div>
        <StatusContainer />
        <LogContainer />
        <FunctionContainer />
      </div>
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
