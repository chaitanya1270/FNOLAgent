import React from "react";

// Groups and labels must match the backend's MANDATORY_FIELDS display names exactly
// so that missingFields highlighting works correctly.
const GROUPS = [
  {
    title: "Policy Information",
    icon:  PolicyIcon,
    fields: [
      { key: "policyNumber",     label: "Policy Number"     },
      { key: "policyholderName", label: "Policyholder Name" },
      { key: "effectiveDates",   label: "Effective Dates"   },
    ],
  },
  {
    title: "Incident Information",
    icon:  IncidentIcon,
    fields: [
      { key: "incidentDate",        label: "Incident Date"        },
      { key: "incidentTime",        label: "Incident Time"        },
      { key: "incidentLocation",    label: "Incident Location"    },
      { key: "incidentDescription", label: "Incident Description" },
    ],
  },
  {
    title: "Involved Parties",
    icon:  PeopleIcon,
    fields: [
      { key: "claimantName",   label: "Claimant Name"   },
      { key: "thirdParties",   label: "Third Parties"   },
      { key: "contactDetails", label: "Contact Details" },
    ],
  },
  {
    title: "Asset Details",
    icon:  AssetIcon,
    fields: [
      { key: "assetType",       label: "Asset Type"       },
      { key: "assetId",         label: "Asset ID"         },
      { key: "estimatedDamage", label: "Estimated Damage" },
    ],
  },
  {
    title: "Other Mandatory Fields",
    icon:  OtherIcon,
    fields: [
      { key: "claimType",       label: "Claim Type"       },
      { key: "attachments",     label: "Attachments"      },
      { key: "initialEstimate", label: "Initial Estimate" },
    ],
  },
];

// All 16 fields are mandatory per the assignment brief.
const MANDATORY_KEYS = new Set([
  "policyNumber", "policyholderName", "effectiveDates",
  "incidentDate", "incidentTime", "incidentLocation", "incidentDescription",
  "claimantName", "thirdParties", "contactDetails",
  "assetType", "assetId", "estimatedDamage",
  "claimType", "attachments", "initialEstimate",
]);

export default function FieldsTable({ fields, missingFields }) {
  const missingLabels = new Set(missingFields ?? []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {GROUPS.map(({ title, icon: Icon, fields: groupFields }) => (
        <div key={title} className="glass-card px-5 py-4">
          {/* Group header */}
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
            <div className="w-7 h-7 rounded-lg bg-accent-50 flex items-center justify-center">
              <Icon />
            </div>
            <p className="text-sm font-bold text-slate-700">{title}</p>
          </div>

          {/* Fields */}
          <dl className="space-y-3">
            {groupFields.map(({ key, label }) => {
              const value       = fields?.[key];
              const isMissing   = missingLabels.has(label);
              const isMandatory = MANDATORY_KEYS.has(key);
              const isEmpty     =
                value === null ||
                value === undefined ||
                value === "" ||
                (Array.isArray(value) && value.length === 0);

              return (
                <div
                  key={key}
                  className={`rounded-lg px-3 py-2.5 ${
                    isMissing ? "bg-red-50 border border-red-200" : "bg-slate-50"
                  }`}
                >
                  <dt className="field-label flex items-center gap-1">
                    {label}
                    {isMandatory && !isMissing && (
                      <span className="w-1 h-1 rounded-full bg-accent-400 inline-block" />
                    )}
                    {isMissing && (
                      <span className="text-red-500 font-bold text-[10px] normal-case tracking-normal ml-1">
                        ✕ missing
                      </span>
                    )}
                  </dt>
                  <dd>
                    {isEmpty ? (
                      <span className="field-empty">—</span>
                    ) : Array.isArray(value) ? (
                      <ul className="space-y-0.5">
                        {value.map((v, i) => (
                          <li key={i} className="field-value flex items-start gap-1.5">
                            <span className="text-slate-300 mt-1">•</span>
                            <span>{v}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <span className="field-value">{value}</span>
                    )}
                  </dd>
                </div>
              );
            })}
          </dl>
        </div>
      ))}
    </div>
  );
}

function PolicyIcon() {
  return (
    <svg className="w-4 h-4 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  );
}

function IncidentIcon() {
  return (
    <svg className="w-4 h-4 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
  );
}

function PeopleIcon() {
  return (
    <svg className="w-4 h-4 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}

function AssetIcon() {
  return (
    <svg className="w-4 h-4 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function OtherIcon() {
  return (
    <svg className="w-4 h-4 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
    </svg>
  );
}
