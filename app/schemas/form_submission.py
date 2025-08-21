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
                            "ID_Number": 100123,
                            "First_Name": "Michael",
                            "Last_Name": "Anderson",
                            "Date_of_Birth": "12031985",
                            "Country": "United States",
                            "Postal_Code": 75001,
                            "Zip_Code": 75001
                        },
                        "Diagnosis": {
                            "ICD10_Code": 10234,
                            "Clinical_Rationale": "Chronic condition requiring continued management",
                            "Previous_Therapies_Tried_and_Failed": "Medication A, Therapy B"
                        },
                        "Service": {
                            "CPT_Code": 12122,
                            "Description": "Physical therapy session",
                            "Place_of_Service": "Outpatient",
                            "Requested_Start_Date": "12022001",
                            "Duration_in_Days": 12,
                            "Priority": "Routine"
                        },
                        "Provider": {
                            "Name": "Dr. Emily Carter",
                            "NPI_Number": 1234567890,
                            "Phone_Number": 5551234567
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
