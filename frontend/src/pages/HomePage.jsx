import React, { useState } from "react";
import UploadZone from "../components/UploadZone";
import LoadingSpinner from "../components/LoadingSpinner";
import ResultsDashboard from "../components/ResultsDashboard";
import ErrorAlert from "../components/ErrorAlert";
import { uploadClaim } from "../services/claimApi";

export default function HomePage({ onNewClaim }) {
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [filename, setFilename] = useState("");

  const handleFileSelect = async (file) => {
    setStatus("uploading");
    setError("");
    setResult(null);
    setFilename(file.name);

    try {
      const data = await uploadClaim(file);
      setResult(data);
      setStatus("success");
      onNewClaim?.({
        filename: file.name,
        route: data.recommendedRoute,
        ts: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      });
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "An unexpected error occurred. Please try again.";
      setError(msg);
      setStatus("error");
    }
  };

  const reset = () => {
    setStatus("idle");
    setResult(null);
    setError("");
    setFilename("");
  };

  return (
    <div className="min-h-full flex flex-col">
      {/* Centered upload view */}
      {status === "idle" && (
        <div className="flex-1 flex flex-col items-center justify-center px-8 py-12">
          <div className="w-full max-w-xl">
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
                Upload Claim Document
              </h1>
              <p className="text-slate-500 text-sm mt-2">
                Upload a PDF or TXT FNOL document to extract, validate, and route the claim automatically.
              </p>
            </div>
            <UploadZone onFileSelect={handleFileSelect} disabled={false} />
          </div>
        </div>
      )}

      {/* Processing pipeline */}
      {status === "uploading" && (
        <div className="flex-1 flex flex-col items-center justify-center px-8 py-12">
          <div className="w-full max-w-xl">
            <LoadingSpinner filename={filename} />
          </div>
        </div>
      )}

      {/* Error */}
      {status === "error" && (
        <div className="flex-1 flex flex-col items-center justify-center px-8 py-12">
          <div className="w-full max-w-xl">
            <ErrorAlert message={error} onDismiss={reset} />
          </div>
        </div>
      )}

      {/* Results */}
      {status === "success" && result && (
        <div className="flex-1 px-8 py-10">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-start justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Claim Results</h1>
                <p className="text-slate-500 text-sm mt-1">Extraction, validation, and routing complete.</p>
              </div>
              <button onClick={reset} className="btn-ghost shrink-0">← New Upload</button>
            </div>
            <ResultsDashboard result={result} filename={filename} onReset={reset} />
          </div>
        </div>
      )}
    </div>
  );
}
