import React, { useState } from "react";
import RouteBadge from "./RouteBadge";
import FieldsTable from "./FieldsTable";

export default function ResultsDashboard({ result, filename }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `claim-result-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header summary */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide font-semibold mb-1">
              Document processed
            </p>
            <p className="font-semibold text-gray-800 dark:text-gray-200">{filename}</p>
          </div>
          <RouteBadge route={result.recommendedRoute} />
        </div>
      </div>

      {/* Routing Reasoning */}
      <div className="card">
        <h2 className="text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-3">
          Routing Reasoning
        </h2>
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          {result.reasoning}
        </p>
      </div>

      {/* Missing Fields */}
      {result.missingFields && result.missingFields.length > 0 && (
        <div className="card border-l-4 border-red-500">
          <h2 className="text-sm font-semibold text-red-600 dark:text-red-400 uppercase tracking-wide mb-3">
            Missing Mandatory Fields ({result.missingFields.length})
          </h2>
          <ul className="flex flex-wrap gap-2">
            {result.missingFields.map((f) => (
              <li
                key={f}
                className="px-3 py-1 text-sm bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg border border-red-200 dark:border-red-800"
              >
                {f}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Extracted Fields */}
      <div className="card">
        <h2 className="text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-4">
          Extracted Fields
        </h2>
        <FieldsTable fields={result.extractedFields} missingFields={result.missingFields} />
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3">
        <button onClick={handleCopy} className="btn-primary text-sm">
          {copied ? "Copied!" : "Copy JSON"}
        </button>
        <button onClick={handleDownload} className="btn-primary text-sm">
          Download JSON
        </button>
      </div>
    </div>
  );
}
