from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class FormSubmissionRequest(BaseModel):
    """Request model for form submission"""
    account_id: Optional[str] = Field(None, description="Custom account ID to fetch data for")
    custom_data: Optional[Dict[str, Any]] = Field(None, description="Additional form data to merge")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "account_id": "1086c0f3-973f-f011-b4cb-7c1e5218e4a2",
                    "custom_data": {
                        "Member": {
                            "ID_Number": "HMA-45893-2",
                            "First_Name": "Suzie",
                            "Last_Name": "Smith",
                            "Date_of_Birth": "01/03/1959",
                            "Country": "USA",
                            "Postal_Code": 40202,
                            "Zip_Code": 40202
                        },
                        "Diagnosis": {
                            "ICD10_Code": "M48.062",
                            "Clinical_Rationale": "Advanced imaging (MRI lumbar spine without contrast – CPT 72148) is medically necessary to evaluate ongoing pain, rule out nerve compression, and determine candidacy for interventional pain management or surgical treatment. Early identification of structural pathology is crucial for preventing further deterioration",
                            "Previous_Therapies_Tried_and_Failed": "Physical Therapy – 6-week program (stretching, strengthening, and mobility exercises)\nOutcome: Minimal improvement; patient reports persistent stiffness and limited range of motion"
                        },
                        "Service": {
                            "CPT_Code": 72148,
                            "Description": "MRI Lumbar Spine w/o Contrast",
                            "Place_of_Service": "Outpatient",
                            "Requested_Start_Date": "08/25/2025",
                            "Duration_in_Days": 1,
                            "Priority": "Routine"
                        },
                        "Provider": {
                            "Name": "Ronald Davidson",
                            "NPI_Number": 1023456789,
                            "Phone_Number": 5615557689
                        }
                    }
                }
            ]
        }
    }

class FormSubmissionResponse(BaseModel):
    """Response model for form submission"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
