import React from "react";
import ReactDOM from "react-dom/client";
import CharacterLoader from "./CharacterLoader";
import { ChatProvider } from "./hooks/useChat";

ReactDOM.createRoot(document.getElementById("root")).render(
    <ChatProvider>
      <CharacterLoader />
    </ChatProvider>
);
