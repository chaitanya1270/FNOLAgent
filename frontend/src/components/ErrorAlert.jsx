import React from "react";

export default function ErrorAlert({ message, onDismiss }) {
  return (
    <div className="max-w-2xl">
      <div className="glass-card border-l-4 border-red-500 px-6 py-5">
        <div className="flex items-start gap-4">
          {/* Icon */}
          <div className="w-10 h-10 rounded-xl bg-red-100 flex items-center justify-center shrink-0">
            <ErrorIcon />
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <p className="font-bold text-slate-900 text-sm">Upload Failed</p>
            <p className="text-sm text-slate-600 mt-1 leading-relaxed">{message}</p>

            <div className="mt-4 flex gap-3">
              {onDismiss && (
                <button onClick={onDismiss} className="btn-accent text-xs px-4 py-2">
                  Try Again
                </button>
              )}
            </div>
          </div>

          {/* Dismiss */}
          {onDismiss && (
            <button
              onClick={onDismiss}
              className="shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
              aria-label="Dismiss"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Hints */}
      <div className="mt-3 px-4 py-3 rounded-lg bg-slate-100 border border-slate-200">
        <p className="text-xs font-semibold text-slate-500 mb-2">Common causes</p>
        <ul className="space-y-1">
          {[
            "File type is not PDF or TXT",
            "File size exceeds 10 MB",
            "The document could not be parsed (scanned image without OCR support)",
            "Azure OpenAI service is temporarily unavailable",
          ].map((hint) => (
            <li key={hint} className="flex items-start gap-2 text-xs text-slate-500">
              <span className="text-slate-300 mt-0.5">•</span>
              {hint}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function ErrorIcon() {
  return (
    <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd"
        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
        clipRule="evenodd" />
    </svg>
  );
}
