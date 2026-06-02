import React from "react";

const ROUTE_CONFIG = {
  "Fast-track": {
    color: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 border-green-200 dark:border-green-800",
    icon: "⚡",
  },
  "Manual Review": {
    color: "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400 border-orange-200 dark:border-orange-800",
    icon: "👤",
  },
  "Investigation Flag": {
    color: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400 border-red-200 dark:border-red-800",
    icon: "🚩",
  },
  "Specialist Queue": {
    color: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 border-blue-200 dark:border-blue-800",
    icon: "🩺",
  },
  "Standard Processing": {
    color: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600",
    icon: "⚙️",
  },
};

export default function RouteBadge({ route }) {
  const config = ROUTE_CONFIG[route] || ROUTE_CONFIG["Standard Processing"];
  return (
    <span
      className={[
        "inline-flex items-center gap-2 px-4 py-2 rounded-full",
        "text-sm font-semibold border",
        config.color,
      ].join(" ")}
    >
      <span>{config.icon}</span>
      {route}
    </span>
  );
}
