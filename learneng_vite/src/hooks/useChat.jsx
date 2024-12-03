import { createContext, useContext, useEffect, useState } from "react";

const backendUrl = "http://localhost:5000";

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const chat = async (message) => {
    setLoading(true);
    const data = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });
    const resp = (await data.json()).messages[0];
    setMessage(resp);
    setLoading(false);
  };

  const [message, setMessage] = useState();
  const [loading, setLoading] = useState(false);

  const initialResponse = async (message) => {
    setLoading(true);
    const response = await fetch("/api/ChatBackend");
    if (response.ok) {
      const data = await response.json();
      setMessage(data);
      setLoading(false);
    }
  };


  const onMessagePlayed = () => {
    setMessage(null);  // Reset the message once it's played
  };

  useEffect(() => {
    if (message) {
      setMessage(message);
    } else {
      setMessage(null);  // Ensures null is set when no message is available
    }
  }, [message]);

  return (
    <ChatContext.Provider
      value={{
        chat,
        initialResponse,
        message,
        onMessagePlayed,
        loading,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
};
