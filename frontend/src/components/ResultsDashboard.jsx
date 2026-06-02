import React, { useState } from "react";
import RouteBadge from "./RouteBadge";
import FieldsTable from "./FieldsTable";

export default function ResultsDashboard({ result, filename, onReset }) {
  const [copied, setCopied] = useState(false);
  const { extractedFields: fields, missingFields, recommendedRoute, reasoning } = result;

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href     = url;
    a.download = `claim-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-5">
      {/* Route status — full-width banner */}
      <RouteBadge
        route={recommendedRoute}
        filename={filename}
        reasoning={reasoning}
        missingCount={missingFields?.length ?? 0}
      />

      {/* Missing fields alert */}
      {missingFields?.length > 0 && (
        <div className="glass-card px-5 py-4 border-l-4 border-red-400">
          <div className="flex items-center gap-2 mb-3">
            <WarnIcon />
            <p className="text-sm font-bold text-red-700">
              {missingFields.length} Mandatory Field{missingFields.length > 1 ? "s" : ""} Missing
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            {missingFields.map((f) => (
              <span
                key={f}
                className="text-xs font-semibold px-3 py-1 rounded-full bg-red-50 text-red-700 border border-red-200"
              >
                {f}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Grouped extracted fields */}
      <FieldsTable fields={fields} missingFields={missingFields} />

      {/* Action bar */}
      <div className="flex items-center gap-3 pt-1">
        <button onClick={handleCopy} className="btn-accent">
          {copied ? "✓ Copied" : "Copy JSON"}
        </button>
        <button onClick={handleDownload} className="btn-ghost">
          Download JSON
        </button>
      </div>
    </div>
  );
}

function WarnIcon() {
  return (
    <svg className="w-4 h-4 text-red-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  );
}
