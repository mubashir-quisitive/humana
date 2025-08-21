from fastapi import APIRouter, HTTPException
from app.schemas.form_submission import FormSubmissionRequest, FormSubmissionResponse
from app.services.form_filling_agent import run_humana_form_filling_agent
from app.services.dataverse_form_data_service import DataverseFormDataService
from app.utils.config import Config
from app.utils.logger import logger

router = APIRouter()

@router.post("/submit-form", response_model=FormSubmissionResponse)
async def submit_form(request: FormSubmissionRequest):
    """Submit form using the Humana form filling agent"""
    try:
        logger.header("🚀 STARTING HUMANA FORM FILLING VIA API")
        logger.start_timer()
        
        # Validate configuration
        logger.progress("🔧 Validating configuration...")
        Config.validate()
        logger.success("✅ Configuration validated successfully")
        
        # Fetch form data from Dataverse
        logger.progress("🔍 Fetching form data from Dataverse...")
        form_data_service = DataverseFormDataService()
        
        if request.account_id:
            # Use custom account ID if provided
            data = form_data_service.fetch_form_data_by_account_id(request.account_id)
        else:
            # Use default account ID from config
            data = form_data_service.fetch_form_data_by_account_id()
        
        if not data:
            raise HTTPException(status_code=404, detail="Failed to fetch form data from Dataverse")
        
        # Merge custom data if provided
        if request.custom_data:
            data.update(request.custom_data)
        
        logger.success("✅ Form data fetched successfully")
        logger.section("📊 FORM DATA RETRIEVED")
        form_data_service.display_form_data(data)
        
        # Run the Humana form filling agent
        logger.section("🤖 STARTING FORM FILLING AGENT")
        logger.progress("🚀 Launching browser automation...")
        await run_humana_form_filling_agent(data)
        logger.success("✅ Form filling agent completed successfully")
        
        logger.end_timer()
        logger.header("🏁 HUMANA FORM FILLING COMPLETED")
        
        return FormSubmissionResponse(
            success=True,
            message="Form submitted successfully",
            data=data
        )
        
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise HTTPException(status_code=400, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"Form submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Form submission failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Humana Form Filling Agent"}
