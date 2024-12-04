import { createContext, useContext, useEffect, useState } from "react";

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [message, setMessage] = useState();
  const [loading, setLoading] = useState(false);
  const [chatStatus, setChatStatus] = useState(false);
  const [nextChat, setNextChat] = useState();

  const getResponse = async (type) => {
    setNextChat(false);
    const response = await fetch("/api/ChatBackend", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure the correct header
      },
      body: JSON.stringify({ response_type: type })
    });

    if (response.ok) {
      const data = await response.json();
      setMessage(data);
      setLoading(false);
      updateChatStatusToNone();
    }
  };

  const getChatStatus = async () => {
    const response = await fetch("http://127.0.0.1:5000/get_status", { method: 'GET' });
    const data = await response.json()
    let status = data.chat_status;
    if (status != chatStatus) {
      setChatStatus(status);
    }
  }

  const updateChatStatusToNone = async () => {
    await fetch("http://127.0.0.1:5000/update_status_to_none", { method: 'POST' });
  }

  const allowNextChat = () => {
    if (!nextChat) {
      setNextChat(true);
    }
  }

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

  useEffect(() => {
    if (chatStatus == "none") {
      setLoading(false);
    } else if (chatStatus == "talking") {
      setLoading(false);
    } else if (chatStatus == "processing") {
      setLoading(true);
    }
  }, [chatStatus]);

  return (
    <ChatContext.Provider
      value={{
        getResponse,
        message,
        onMessagePlayed,
        loading,
        getChatStatus,
        chatStatus,
        allowNextChat,
        nextChat
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
