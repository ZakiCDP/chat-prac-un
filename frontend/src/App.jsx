import React, { useState, useEffect } from "react";
import AuthForm from "./components/AuthForm";
import Chat from "./components/Chat";
import "./styles.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");

  const handleLogin = (user) => {
    setIsAuthenticated(true);
    setUsername(user);
  };

  return (
    <div className="app">
      {isAuthenticated ? (
        <Chat username={username} />
      ) : (
        <AuthForm onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
