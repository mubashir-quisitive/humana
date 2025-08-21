from pydantic import BaseModel, Field
from typing import Optional

class TrackerAgentRequest(BaseModel):
    """Request model for tracker agent"""
    custom_tracking_id: Optional[str] = Field(None, description="Optional custom PA request ID to track")
    custom_interval: Optional[int] = Field(None, description="Optional custom check interval in seconds")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "custom_tracking_id": "PA-130810002",
                    "custom_interval": 15
                },
                {
                    "custom_tracking_id": None,
                    "custom_interval": None
                }
            ]
        }
    }

class TrackerAgentResponse(BaseModel):
    """Response model for tracker agent"""
    success: bool
    message: str
    data: dict
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "message": "Tracker Agent has started",
                    "data": {
                        "status": "tracking",
                        "tracking_id": "PA-14091005229",
                        "interval_seconds": 10
                    }
                }
            ]
        }
    }
