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
                        "patient_name": "John Doe",
                        "diagnosis": "Hypertension",
                        "medication": "Lisinopril"
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
