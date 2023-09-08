import { useEffect } from "react";
import { sio } from "./config";
import { ChakraProvider } from "@chakra-ui/react";
import LogContainer from "./components/logdiv.com";

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
    </div>
  );
}

function Wrapper() {
  return (
    <ChakraProvider>
      <App />
    </ChakraProvider>
  );
}

export default Wrapper;
