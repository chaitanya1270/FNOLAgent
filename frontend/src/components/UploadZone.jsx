import React, { useCallback, useRef, useState } from "react";

const ALLOWED_EXT = [".pdf", ".txt"];
const ALLOWED_TYPES = ["application/pdf", "text/plain"];

export default function UploadZone({ onFileSelect, disabled }) {
  const [dragOver, setDragOver] = useState(false);
  const [fileError, setFileError] = useState("");
  const inputRef = useRef(null);

  const validate = (file) => {
    if (!file) return "No file selected.";
    const ext = "." + file.name.split(".").pop().toLowerCase();
    if (!ALLOWED_EXT.includes(ext) && !ALLOWED_TYPES.includes(file.type))
      return `"${ext}" is not supported. Upload a PDF or TXT file.`;
    if (file.size > 10 * 1024 * 1024) return "File exceeds the 10 MB limit.";
    if (file.size === 0) return "The selected file is empty.";
    return "";
  };

  const handleFile = useCallback(
    (file) => {
      const err = validate(file);
      if (err) { setFileError(err); return; }
      setFileError("");
      onFileSelect(file);
    },
    [onFileSelect]
  );

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (!disabled) handleFile(e.dataTransfer.files[0]);
  };

  const onInputChange = (e) => {
    handleFile(e.target.files[0]);
    e.target.value = "";
  };

  return (
    <div className="w-full">
      {/* Drop area */}
      <div
        onDragEnter={(e) => { e.preventDefault(); if (!disabled) setDragOver(true); }}
        onDragLeave={(e) => { e.preventDefault(); setDragOver(false); }}
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        className={[
          "relative rounded-2xl border-2 border-dashed transition-all cursor-pointer",
          "flex flex-col items-center justify-center gap-6 py-20 px-8",
          dragOver
            ? "border-accent-500 bg-accent-50"
            : "border-slate-300 bg-white hover:border-accent-400 hover:bg-slate-50/80",
          disabled && "opacity-50 pointer-events-none",
        ].join(" ")}
      >
        {/* Icon */}
        <div className={[
          "w-20 h-20 rounded-2xl flex items-center justify-center transition-colors shadow-sm",
          dragOver ? "bg-accent-100 shadow-accent-100" : "bg-slate-100",
        ].join(" ")}>
          <CloudUploadIcon className={`w-10 h-10 ${dragOver ? "text-accent-600" : "text-slate-400"}`} />
        </div>

        {/* Text */}
        <div className="text-center space-y-1.5">
          <p className="text-slate-800 font-semibold text-lg">
            {dragOver ? "Release to upload" : "Drop your FNOL document here"}
          </p>
          <p className="text-slate-400 text-sm">
            Supports <span className="font-medium text-slate-500">PDF</span> and <span className="font-medium text-slate-500">TXT</span> — maximum 10 MB
          </p>
        </div>

        {/* Divider */}
        <div className="flex items-center gap-3 w-40">
          <div className="flex-1 h-px bg-slate-200" />
          <span className="text-xs text-slate-300 font-medium">or</span>
          <div className="flex-1 h-px bg-slate-200" />
        </div>

        {/* CTA */}
        <button
          type="button"
          disabled={disabled}
          onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
          className="btn-accent px-8 py-2.5 text-sm font-semibold shadow-sm"
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
        <div className="mt-3 flex items-center gap-2 text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl px-4 py-3">
          <ErrorIcon />
          {fileError}
        </div>
      )}

      {/* Format hints */}
      <div className="mt-4 grid grid-cols-2 gap-3">
        {[
          { ext: "PDF", desc: "Digital or scanned — OCR supported" },
          { ext: "TXT", desc: "Plain-text FNOL document" },
        ].map(({ ext, desc }) => (
          <div key={ext} className="glass-card px-4 py-3 flex items-center gap-3">
            <span className="text-xs font-bold text-accent-600 bg-accent-50 border border-accent-200 rounded-md px-2 py-0.5">
              .{ext}
            </span>
            <span className="text-xs text-slate-500">{desc}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function CloudUploadIcon({ className }) {
  return (
    <svg className={`w-8 h-8 ${className}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
  );
}

function ErrorIcon() {
  return (
    <svg className="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  );
}
