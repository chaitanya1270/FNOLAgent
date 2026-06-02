import React from "react";

export default function LoadingSpinner({ message = "Processing document…" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12">
      <div className="w-12 h-12 border-4 border-brand-200 dark:border-brand-800 border-t-brand-600 rounded-full animate-spin" />
      <p className="text-sm text-gray-500 dark:text-gray-400">{message}</p>
    </div>
  );
}
