import { useEffect, useRef, useState } from "react";
import { useChat } from "../hooks/useChat";

export const UI = ({ hidden, ...props }) => {
  const input = useRef();
  const { chat, loading, message } = useChat();

  const sendMessage = () => {
    const text = input.current.value;
    if (!loading && !message) {
      chat(text);
      input.current.value = "";
    }
  };


  const { initialResponse } = useChat();

  const [clicked, setClicked] = useState(false);

  const start = () => {
    console.log('clicked');
    initialResponse();
    setClicked(true);
  }

  useEffect(() => {
    if (!loading && !message) {
     setClicked(false);
    }
  }, [loading, message])

  if (hidden) {
    return null;
  }

  return (
    <>
      <div className="fixed top-0 left-0 right-0 bottom-0 z-10 flex justify-between p-4 flex-col pointer-events-none">
        {/* <div className="flex items-center gap-2 pointer-events-auto max-w-screen-sm w-full mx-auto">
          <input
            className="w-full placeholder:text-gray-800 placeholder:italic p-4 rounded-md bg-opacity-50 bg-white backdrop-blur-md"
            placeholder="Type a message..."
            ref={input}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />
          <button
            disabled={loading || message}
            onClick={sendMessage}
            className={`bg-pink-500 hover:bg-pink-600 text-white p-4 px-10 font-semibold uppercase rounded-md ${
              loading || message ? "cursor-not-allowed opacity-30" : ""
            }`}
          >
            Send
          </button>
        </div> */}
        <div className="flex items-end gap-2 pointer-events-auto max-w-screen-sm w-full mx-auto">
          <button
            disabled={clicked}
            onClick={() => {start()}}
            className={`bg-blue-500 hover:bg-blue-600 text-white p-4 px-10 font-semibold uppercase rounded-md`}
          >
            Start
          </button>
        </div>
      </div>
    </>
  );
};
