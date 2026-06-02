import React, { useState } from "react";
import UploadZone from "../components/UploadZone";
import LoadingSpinner from "../components/LoadingSpinner";
import ResultsDashboard from "../components/ResultsDashboard";
import ErrorAlert from "../components/ErrorAlert";
import { uploadClaim } from "../services/claimApi";

export default function HomePage() {
  const [status, setStatus] = useState("idle"); // idle | uploading | success | error
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [filename, setFilename] = useState("");
  const [history, setHistory] = useState([]);

  const handleFileSelect = async (file) => {
    setStatus("uploading");
    setError("");
    setResult(null);
    setFilename(file.name);

    try {
      const data = await uploadClaim(file);
      setResult(data);
      setStatus("success");
      setHistory((prev) => [
        { filename: file.name, route: data.recommendedRoute, ts: new Date().toLocaleTimeString() },
        ...prev.slice(0, 4),
      ]);
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
  };

  return (
    <main className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      {/* Upload card */}
      <div className="card">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
              Upload FNOL Document
            </h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
              PDF or TXT — up to 10 MB
            </p>
          </div>
          {status !== "idle" && (
            <button
              onClick={reset}
              className="text-sm text-brand-600 hover:underline dark:text-brand-400"
            >
              Upload new
            </button>
          )}
        </div>

        <UploadZone onFileSelect={handleFileSelect} disabled={status === "uploading"} />
      </div>

      {/* States */}
      {status === "uploading" && (
        <div className="card">
          <LoadingSpinner message="Extracting claim data with Azure OpenAI…" />
        </div>
      )}

      {status === "error" && (
        <ErrorAlert message={error} onDismiss={reset} />
      )}

      {status === "success" && result && (
        <ResultsDashboard result={result} filename={filename} />
      )}

      {/* Upload History */}
      {history.length > 0 && (
        <div className="card">
          <h2 className="text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-3">
            Recent Uploads
          </h2>
          <ul className="divide-y divide-gray-100 dark:divide-gray-700">
            {history.map((h, i) => (
              <li key={i} className="py-2 flex items-center justify-between text-sm">
                <span className="text-gray-700 dark:text-gray-300 truncate max-w-xs">{h.filename}</span>
                <div className="flex items-center gap-3 shrink-0">
                  <span className="text-gray-400 dark:text-gray-500 text-xs">{h.ts}</span>
                  <span className="font-medium text-gray-600 dark:text-gray-400 text-xs">{h.route}</span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
