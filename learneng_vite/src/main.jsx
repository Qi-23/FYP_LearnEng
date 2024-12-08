import React from "react";
import ReactDOM from "react-dom/client";
import CharacterLoader from "./CharacterLoader";
import { ChatProvider } from "./hooks/useChat";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
    <ChatProvider>
      <CharacterLoader />
    </ChatProvider>
);
