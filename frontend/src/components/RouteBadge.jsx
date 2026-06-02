import React from "react";

const ROUTE_CONFIG = {
  "Fast-track": {
    bg:      "bg-emerald-50",
    border:  "border-emerald-200",
    badge:   "bg-emerald-500 text-white",
    icon:    FastIcon,
    label:   "Fast-track",
    sub:     "Eligible for expedited automated processing",
  },
  "Manual Review": {
    bg:      "bg-amber-50",
    border:  "border-amber-200",
    badge:   "bg-amber-500 text-white",
    icon:    ReviewIcon,
    label:   "Manual Review",
    sub:     "A human adjuster will complete missing information",
  },
  "Investigation Flag": {
    bg:      "bg-red-50",
    border:  "border-red-200",
    badge:   "bg-red-600 text-white",
    icon:    FlagIcon,
    label:   "Investigation Flag",
    sub:     "Potential fraud indicators detected — requires investigation",
  },
  "Specialist Queue": {
    bg:      "bg-sky-50",
    border:  "border-sky-200",
    badge:   "bg-sky-600 text-white",
    icon:    SpecialistIcon,
    label:   "Specialist Queue",
    sub:     "Injury claim routed to a specialist adjuster",
  },
  "Standard Processing": {
    bg:      "bg-slate-50",
    border:  "border-slate-200",
    badge:   "bg-slate-600 text-white",
    icon:    StandardIcon,
    label:   "Standard Processing",
    sub:     "Routed through the standard claims workflow",
  },
};

export default function RouteBadge({ route, filename, reasoning, missingCount }) {
  const cfg = ROUTE_CONFIG[route] ?? ROUTE_CONFIG["Standard Processing"];
  const Icon = cfg.icon;

  return (
    <div className={`glass-card ${cfg.bg} border ${cfg.border} px-6 py-5`}>
      {/* Top row: filename + route badge */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="min-w-0">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
            Document Processed
          </p>
          <p className="text-sm font-semibold text-slate-700 truncate">{filename}</p>
        </div>
        <span className={`shrink-0 inline-flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-bold ${cfg.badge}`}>
          <Icon className="w-4 h-4" />
          {cfg.label}
        </span>
      </div>

      {/* Divider */}
      <div className={`border-t ${cfg.border} my-4`} />

      {/* Routing reasoning */}
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-lg bg-white/70 border border-white flex items-center justify-center shrink-0 mt-0.5">
          <QuoteIcon />
        </div>
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
            Routing Reasoning
          </p>
          <p className="text-sm text-slate-700 leading-relaxed">{reasoning}</p>
        </div>
      </div>
    </div>
  );
}

function FastIcon({ className }) {
  return (
    <svg className={className} fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function ReviewIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  );
}

function FlagIcon({ className }) {
  return (
    <svg className={className} fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 7l2.55 2.4A1 1 0 0116 11H6a1 1 0 00-1 1v3a1 1 0 11-2 0V6z" clipRule="evenodd" />
    </svg>
  );
}

function SpecialistIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
    </svg>
  );
}

function StandardIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
    </svg>
  );
}

function QuoteIcon() {
  return (
    <svg className="w-4 h-4 text-slate-400" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
    </svg>
  );
}
