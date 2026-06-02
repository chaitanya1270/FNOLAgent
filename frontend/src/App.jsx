import React, { useState } from "react";
import Sidebar from "./components/Header";
import HomePage from "./pages/HomePage";

export default function App() {
  const [history, setHistory] = useState([]);

  const addToHistory = (entry) => {
    setHistory((prev) => [entry, ...prev.slice(0, 9)]);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-100">
      <Sidebar history={history} />
      <div className="flex-1 overflow-y-auto">
        <HomePage onNewClaim={addToHistory} />
      </div>
    </div>
  );
}
