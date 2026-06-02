from typing import List, Optional
from pydantic import BaseModel, Field


class ExtractedFields(BaseModel):
    policyNumber: Optional[str] = Field(default=None, description="Insurance policy number")
    policyholderName: Optional[str] = Field(default=None, description="Full name of the policyholder")
    effectiveDates: Optional[str] = Field(default=None, description="Policy effective date range")
    incidentDate: Optional[str] = Field(default=None, description="Date the incident occurred")
    incidentTime: Optional[str] = Field(default=None, description="Time the incident occurred")
    incidentLocation: Optional[str] = Field(default=None, description="Location where incident occurred")
    incidentDescription: Optional[str] = Field(default=None, description="Detailed description of the incident")
    claimantName: Optional[str] = Field(default=None, description="Name of the person filing the claim")
    thirdParties: List[str] = Field(default_factory=list, description="Names of third parties involved")
    contactDetails: Optional[str] = Field(default=None, description="Contact information of claimant")
    assetType: Optional[str] = Field(default=None, description="Type of asset (vehicle, property, etc.)")
    assetId: Optional[str] = Field(default=None, description="Asset identifier (VIN, property address, etc.)")
    estimatedDamage: Optional[str] = Field(default=None, description="Estimated damage amount in USD")
    claimType: Optional[str] = Field(default=None, description="Type of claim (auto, property, injury, etc.)")
    attachments: List[str] = Field(default_factory=list, description="List of attached documents")
    initialEstimate: Optional[str] = Field(default=None, description="Initial cost estimate for the claim")


class ClaimExtractionResult(BaseModel):
    extractedFields: ExtractedFields
    missingFields: List[str] = Field(default_factory=list)
    recommendedRoute: str = Field(default="Standard Processing")
    reasoning: str = Field(default="")
