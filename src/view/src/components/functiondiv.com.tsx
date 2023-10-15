import Draggable from "react-draggable";
import { sio } from "../config";
import style from "./styles/functiondiv.module.scss";
import { useEffect, useState } from "react";
import { log } from "./logdiv.com";

function FunctionContainer() {
  const [genAudioString, setGenAudioString] = useState("");
  const [genAudioBytes, setGenAudioBytes] = useState<string>();

  useEffect(() => {
    return () => {
      URL.revokeObjectURL(genAudioBytes!);
    };
  }, [genAudioBytes]);

  return (
    <Draggable>
      <div className={style.div}>
        <div>
          <input
            value={genAudioString}
            onChange={(e) => setGenAudioString(e.target.value)}
            placeholder="Text"
          ></input>
          <button
            onClick={() => {
              if (genAudioString.trim() === "") return;
              sio.emit("audio_gen", genAudioString, (b: any) => {
                console.log(b);
                const file = new Blob([b], {
                  type: "audio/wave",
                });
                console.log(file);
                const location = URL.createObjectURL(file);
                console.log(location);
                setGenAudioBytes(location);
              });
            }}
          >
            Generate Audio
          </button>
          <audio src={genAudioBytes} />
        </div>
      </div>
    </Draggable>
  );
}

export default FunctionContainer;
