import { useEffect, useState } from "react";
import { customTheme, sio } from "./config";
import { ChakraProvider } from "@chakra-ui/react";
import LogContainer from "./components/logdiv.com";

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
          sio.emit("log", input);
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
              alert(response);
            }
          );
        }}
      >
        Model Test
      </button>
      <LogContainer />
      <SendMessage />
    </div>
  );
}

function Wrapper() {
  return (
    <ChakraProvider theme={customTheme}>
      <App />
    </ChakraProvider>
  );
}

export default Wrapper;
