from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.form_submission import FormSubmissionRequest, FormSubmissionResponse
from app.services.form_filling_agent import run_humana_form_filling_agent
from app.services.dataverse_form_data_service import DataverseFormDataService
from app.utils.config import Config
from app.utils.logger import logger

router = APIRouter()

async def process_form_submission_background(request: FormSubmissionRequest):
    """Background task for form submission processing"""
    try:
        logger.header("🚀 STARTING HUMANA FORM FILLING IN BACKGROUND")
        logger.start_timer()
        
        # Validate configuration
        Config.validate()
        
        # Fetch form data from Dataverse
        form_data_service = DataverseFormDataService()
        data = form_data_service.fetch_form_data_by_account_id(request.account_id)
        
        if not data:
            logger.error("Failed to fetch form data from Dataverse")
            return
        
        # Merge custom data if provided
        if request.custom_data:
            data.update(request.custom_data)
        
        # Run the Humana form filling agent
        await run_humana_form_filling_agent(data)
        logger.success("✅ Form filling agent completed successfully")
        logger.end_timer()
        
    except Exception as e:
        logger.error(f"Background form submission failed: {e}")

@router.post("/submit-form", response_model=FormSubmissionResponse)
async def submit_form(request: FormSubmissionRequest, background_tasks: BackgroundTasks):
    """Submit form - returns immediately, processes in background"""
    # Add form submission to background tasks
    background_tasks.add_task(process_form_submission_background, request)
    
    return FormSubmissionResponse(
        success=True,
        message="Form submission started in background",
        data={"status": "processing", "request_id": f"req_{hash(str(request))}"}
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Humana Form Filling Agent"}
