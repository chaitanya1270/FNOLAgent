import React from "react";

export default function ErrorAlert({ message, onDismiss }) {
  return (
    <div className="card border-l-4 border-red-500 bg-red-50 dark:bg-red-900/10">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3">
          <span className="text-red-500 text-xl mt-0.5">⚠</span>
          <div>
            <p className="font-semibold text-red-700 dark:text-red-400">Upload Failed</p>
            <p className="text-sm text-red-600 dark:text-red-300 mt-1">{message}</p>
          </div>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-red-400 hover:text-red-600 dark:hover:text-red-300 text-lg leading-none"
          >
            ×
          </button>
        )}
      </div>
    </div>
  );
}
