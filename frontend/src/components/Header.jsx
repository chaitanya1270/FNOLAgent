import React from "react";

const ROUTE_COLORS = {
  "Fast-track":         "text-emerald-400",
  "Manual Review":      "text-amber-400",
  "Investigation Flag": "text-red-400",
  "Specialist Queue":   "text-sky-400",
  "Standard Processing":"text-slate-400",
};

const NAV = [
  { icon: UploadIcon, label: "Upload Claim", active: true },
];

export default function Sidebar({ history = [] }) {
  return (
    <aside className="w-60 bg-[#16162a] flex flex-col shrink-0 h-full select-none">
      {/* Logo */}
      <div className="px-5 pt-6 pb-5 border-b border-white/8">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent-500 to-accent-700 flex items-center justify-center shrink-0">
            <ShieldIcon />
          </div>
          <div>
            <p className="text-white font-bold text-sm leading-none tracking-tight">FNOLAgent</p>
            <p className="text-slate-500 text-xs mt-0.5">Claims Intelligence</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="px-3 pt-4 pb-2 space-y-0.5">
        <p className="text-slate-600 text-[10px] font-bold uppercase tracking-widest px-3 mb-2">
          Navigation
        </p>
        {NAV.map(({ icon: Icon, label, active }) => (
          <div key={label} className={active ? "sidebar-item-active" : "sidebar-item"}>
            <Icon className={`w-4 h-4 ${active ? "text-accent-400" : "text-slate-500"}`} />
            <span>{label}</span>
            {active && (
              <span className="ml-auto w-1.5 h-1.5 rounded-full bg-accent-400" />
            )}
          </div>
        ))}
      </nav>

      {/* Recent Claims */}
      <div className="flex-1 overflow-hidden flex flex-col px-3 pt-4 border-t border-white/8 mt-3">
        <p className="text-slate-600 text-[10px] font-bold uppercase tracking-widest px-3 mb-3">
          Recent Claims
        </p>
        {history.length === 0 ? (
          <div className="px-3 py-4 rounded-lg border border-dashed border-white/10 text-center">
            <p className="text-slate-600 text-xs">No uploads yet</p>
          </div>
        ) : (
          <ul className="space-y-0.5 overflow-y-auto">
            {history.map((h, i) => (
              <li
                key={i}
                className="px-3 py-2 rounded-lg hover:bg-white/5 transition-colors"
              >
                <p className="text-slate-300 text-xs font-medium truncate leading-none">{h.filename}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-slate-600 text-[10px]">{h.ts}</span>
                  <span className={`text-[10px] font-semibold ${ROUTE_COLORS[h.route] || "text-slate-400"}`}>
                    {h.route}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* System status */}
      <div className="px-5 py-4 border-t border-white/8">
        <div className="flex items-center gap-2 mb-1">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse-slow" />
          <span className="text-slate-400 text-xs font-medium">System Online</span>
        </div>
        <p className="text-slate-600 text-[10px]">GPT-4.1 · Azure OpenAI</p>
      </div>
    </aside>
  );
}

function ShieldIcon() {
  return (
    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M10 1.5l7 3v4.5c0 4.25-3.5 7.5-7 8.5C6.5 16.5 3 13.25 3 9V4.5l7-3z" clipRule="evenodd" />
    </svg>
  );
}

function UploadIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1M12 12V4m0 0L9 7m3-3l3 3" />
    </svg>
  );
}

function GridIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M3 7h5v5H3V7zm0 9h5v5H3v-5zm9-9h5v5h-5V7zm0 9h5v5h-5v-5z" />
    </svg>
  );
}

function ChartIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6m6 0V9a2 2 0 012-2h2a2 2 0 012 2v10m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14" />
    </svg>
  );
}

function GearIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}
