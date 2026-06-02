import React, { useEffect, useState } from "react";

const STEPS = [
  { label: "Parsing document", desc: "Extracting raw text from the uploaded file" },
  { label: "AI extraction",    desc: "Identifying 16 claim fields via GPT-4.1" },
  { label: "Validation",       desc: "Checking mandatory fields for completeness" },
  { label: "Routing decision", desc: "Applying priority rules to determine route" },
];

export default function LoadingSpinner({ filename }) {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setActiveStep((s) => (s < STEPS.length - 1 ? s + 1 : s));
    }, 1800);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="max-w-2xl">
      {/* File banner */}
      <div className="glass-card px-5 py-4 mb-6 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-accent-50 border border-accent-200 flex items-center justify-center shrink-0">
          <FileIcon />
        </div>
        <div className="min-w-0">
          <p className="text-sm font-semibold text-slate-800 truncate">{filename}</p>
          <p className="text-xs text-slate-400 mt-0.5">Processing in progress&hellip;</p>
        </div>
        <div className="ml-auto shrink-0">
          <Spinner />
        </div>
      </div>

      {/* Pipeline steps */}
      <div className="glass-card px-6 py-5">
        <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-5">
          Processing Pipeline
        </p>
        <ol className="space-y-5">
          {STEPS.map((step, i) => {
            const done   = i < activeStep;
            const active = i === activeStep;
            return (
              <li key={step.label} className="flex items-start gap-4">
                {/* Step indicator */}
                <div className="shrink-0 flex flex-col items-center">
                  {done ? (
                    <div className="step-dot-done">
                      <CheckIcon />
                    </div>
                  ) : active ? (
                    <div className="step-dot-active">
                      <span className="w-3 h-3 rounded-full bg-white/80" />
                    </div>
                  ) : (
                    <div className="step-dot-pending">
                      <span className="text-xs font-bold text-slate-400">{i + 1}</span>
                    </div>
                  )}
                  {i < STEPS.length - 1 && (
                    <div className={`w-px flex-1 mt-1 min-h-[20px] ${done ? "bg-emerald-300" : "bg-slate-200"}`} />
                  )}
                </div>

                {/* Step text */}
                <div className="pt-1 pb-4">
                  <p className={`text-sm font-semibold leading-none ${
                    done ? "text-emerald-600" : active ? "text-slate-900" : "text-slate-400"
                  }`}>
                    {step.label}
                  </p>
                  <p className={`text-xs mt-1 ${
                    done || active ? "text-slate-500" : "text-slate-300"
                  }`}>
                    {step.desc}
                  </p>
                </div>
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}

function Spinner() {
  return (
    <svg className="w-5 h-5 animate-spin text-accent-600" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
    </svg>
  );
}

function FileIcon() {
  return (
    <svg className="w-5 h-5 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  );
}
