import Draggable from "react-draggable";
import { sio } from "../config";
import style from "./styles/chatdiv.module.scss";
import { useEffect, useState } from "react";

type ChatMessage = {
  bot: boolean;
  message: string;
};

function ChatContainer() {
  const [chatInput, setChatInput] = useState<string>();
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      bot: true,
      message: `Hello, my name is Robert. I am an artificial chatbot used for the International Baccalaureate personal project. I am not alive, therefore I cannot provide you with present knowledge. However, I will try to have a conversation with you. It is nice to meet you.`,
    },
  ]);
  const [lock, setLock] = useState<boolean>(false);
  const [chatCode, setChatCode] = useState<string>("");

  return (
    <Draggable>
      <div className={style.div}>
        <div>
          <button
            onClick={() => {
              sio.emit("llm-new_chat", undefined, (id: string) => {
                setChatCode(id);
                setChatMessages([
                  {
                    bot: true,
                    message: `Hello, my name is Robert. I am an artificial chatbot used for the International Baccalaureate personal project. I am not alive, therefore I cannot provide you with present knowledge. However, I will try to have a conversation with you. It is nice to meet you.`,
                  },
                ]);
              });
            }}
          >
            New Chat
          </button>
          <p>Current Chat Code: {chatCode === "" ? "No code" : chatCode}</p>
        </div>
        <div>
          {chatMessages.slice().map((v, i) => {
            return (
              <p key={i}>
                {v.bot ? "[Bot]" : "[Self]"} - {v.message}
              </p>
            );
          })}
        </div>
        <div>
          <input
            type="text"
            onChange={(e) => setChatInput(e.target.value)}
            value={chatInput}
          />
          <button
            onClick={() => {
              const copy = chatInput;
              console.log({ lock, chatCode, chatInput, copy });
              if (lock || chatCode === "" || chatInput === "" || copy === "")
                return;
              setLock(true);
              setChatInput("");

              const s: ChatMessage = {
                bot: false,
                message: copy as string,
              };

              setChatMessages([...chatMessages, s]);

              sio.emit(
                "llm-send_message",
                copy,
                (response: string | boolean) => {
                  setLock(false);
                  if (typeof response === "boolean") {
                    alert("No chat code is present");
                  } else {
                    console.log(response);

                    const x: ChatMessage = {
                      bot: true,
                      message: response,
                    };

                    setChatMessages([...chatMessages, s, x]);
                  }
                  // TODO
                }
              );
            }}
          >
            Send Chat
          </button>
        </div>
      </div>
    </Draggable>
  );
}

export default ChatContainer;
