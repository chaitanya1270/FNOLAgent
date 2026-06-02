import React from "react";

export default function Header({ darkMode, onToggleDark }) {
  return (
    <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4">
      <div className="max-w-5xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-brand-600 rounded-xl flex items-center justify-center text-white font-bold text-sm">
            FA
          </div>
          <div>
            <h1 className="font-bold text-gray-900 dark:text-white text-lg leading-tight">
              FNOLAgent
            </h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Autonomous Insurance Claims Processing
            </p>
          </div>
        </div>

        <button
          onClick={onToggleDark}
          aria-label="Toggle dark mode"
          className="p-2 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          {darkMode ? "☀" : "☾"}
        </button>
      </div>
    </header>
  );
}
