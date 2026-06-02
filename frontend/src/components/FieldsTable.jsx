import React from "react";

const FIELD_LABELS = {
  policyNumber: "Policy Number",
  policyholderName: "Policyholder Name",
  effectiveDates: "Effective Dates",
  incidentDate: "Incident Date",
  incidentTime: "Incident Time",
  incidentLocation: "Incident Location",
  incidentDescription: "Incident Description",
  claimantName: "Claimant Name",
  thirdParties: "Third Parties",
  contactDetails: "Contact Details",
  assetType: "Asset Type",
  assetId: "Asset ID",
  estimatedDamage: "Estimated Damage",
  claimType: "Claim Type",
  attachments: "Attachments",
  initialEstimate: "Initial Estimate",
};

export default function FieldsTable({ fields, missingFields }) {
  const missingSet = new Set(missingFields);

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-700">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-gray-50 dark:bg-gray-800">
            <th className="text-left px-4 py-3 font-semibold text-gray-600 dark:text-gray-400 w-2/5">Field</th>
            <th className="text-left px-4 py-3 font-semibold text-gray-600 dark:text-gray-400">Value</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
          {Object.entries(FIELD_LABELS).map(([key, label]) => {
            const value = fields[key];
            const isMissing = missingSet.has(label);
            const isEmpty = value === null || value === undefined || value === "" ||
              (Array.isArray(value) && value.length === 0);

            return (
              <tr
                key={key}
                className={isMissing ? "bg-red-50 dark:bg-red-900/10" : "bg-white dark:bg-gray-900"}
              >
                <td className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300 align-top">
                  <span>{label}</span>
                  {isMissing && (
                    <span className="ml-2 text-xs text-red-500 font-semibold">(missing)</span>
                  )}
                </td>
                <td className="px-4 py-3 text-gray-600 dark:text-gray-400">
                  {isEmpty ? (
                    <span className="italic text-gray-400 dark:text-gray-600">—</span>
                  ) : Array.isArray(value) ? (
                    <ul className="list-disc list-inside space-y-0.5">
                      {value.map((v, i) => <li key={i}>{v}</li>)}
                    </ul>
                  ) : (
                    <span>{value}</span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
