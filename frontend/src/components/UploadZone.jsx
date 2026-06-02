import React, { useCallback, useRef, useState } from "react";

const ALLOWED_TYPES = ["application/pdf", "text/plain"];
const ALLOWED_EXT = [".pdf", ".txt"];

export default function UploadZone({ onFileSelect, disabled }) {
  const [dragActive, setDragActive] = useState(false);
  const [fileError, setFileError] = useState("");
  const inputRef = useRef(null);

  const validate = (file) => {
    if (!file) return "No file selected.";
    const ext = "." + file.name.split(".").pop().toLowerCase();
    if (!ALLOWED_EXT.includes(ext) && !ALLOWED_TYPES.includes(file.type)) {
      return `Unsupported file type "${ext}". Only PDF and TXT are accepted.`;
    }
    if (file.size > 10 * 1024 * 1024) return "File exceeds 10 MB limit.";
    if (file.size === 0) return "File is empty.";
    return "";
  };

  const handleFile = useCallback(
    (file) => {
      const error = validate(file);
      if (error) {
        setFileError(error);
        return;
      }
      setFileError("");
      onFileSelect(file);
    },
    [onFileSelect]
  );

  const onDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (disabled) return;
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const onInputChange = (e) => {
    const file = e.target.files[0];
    handleFile(file);
    e.target.value = "";
  };

  return (
    <div className="space-y-3">
      <div
        onDragEnter={(e) => { e.preventDefault(); if (!disabled) setDragActive(true); }}
        onDragLeave={(e) => { e.preventDefault(); setDragActive(false); }}
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        className={[
          "flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed",
          "p-10 cursor-pointer transition-all",
          dragActive
            ? "border-brand-500 bg-brand-50 dark:bg-brand-900/20"
            : "border-gray-300 dark:border-gray-600 hover:border-brand-400 dark:hover:border-brand-500 bg-gray-50 dark:bg-gray-800/40",
          disabled && "opacity-50 cursor-not-allowed",
        ].join(" ")}
      >
        <UploadIcon />
        <div className="text-center">
          <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Drag &amp; drop your FNOL document here
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Supports PDF and TXT — max 10 MB
          </p>
        </div>
        <button
          type="button"
          disabled={disabled}
          className="btn-primary text-sm"
          onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
        >
          Browse File
        </button>
      </div>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt,application/pdf,text/plain"
        className="hidden"
        onChange={onInputChange}
        disabled={disabled}
      />

      {fileError && (
        <p className="text-sm text-red-600 dark:text-red-400 flex items-center gap-1">
          <span>⚠</span> {fileError}
        </p>
      )}
    </div>
  );
}

function UploadIcon() {
  return (
    <svg className="w-12 h-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1M12 12V4m0 0L9 7m3-3l3 3" />
    </svg>
  );
}
