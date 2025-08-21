from fastapi import APIRouter, HTTPException, BackgroundTasks
import uuid
from app.schemas.form_submission import FormSubmissionRequest, FormSubmissionResponse
from app.services.form_filling_agent import run_humana_form_filling_agent
from app.services.dataverse_form_data_service import DataverseFormDataService
from app.utils.config import Config
from app.utils.logger import logger
from app.utils.agent_tracker import agent_tracker

router = APIRouter()

async def process_form_submission_background(request: FormSubmissionRequest, request_id: str):
    """Background task for form submission processing"""
    try:
        agent_tracker.log_action(request_id, "🚀 STARTING HUMANA FORM FILLING IN BACKGROUND")
        logger.header("🚀 STARTING HUMANA FORM FILLING IN BACKGROUND")
        logger.start_timer()
        
        # Validate configuration
        agent_tracker.log_action(request_id, "🔧 Validating configuration")
        Config.validate()
        
        # Fetch form data from Dataverse
        agent_tracker.log_action(request_id, "🔍 Fetching form data from Dataverse")
        form_data_service = DataverseFormDataService()
        data = form_data_service.fetch_form_data_by_account_id(request.account_id)
        
        if not data:
            agent_tracker.log_action(request_id, "❌ Failed to fetch form data from Dataverse")
            logger.error("Failed to fetch form data from Dataverse")
            return
        
        # Merge custom data if provided
        if request.custom_data:
            data.update(request.custom_data)
        
        # Run the Humana form filling agent
        agent_tracker.log_action(request_id, "🤖 Starting form filling agent")
        await run_humana_form_filling_agent(data, request_id)
        agent_tracker.log_action(request_id, "✅ Form filling agent completed successfully")
        logger.success("✅ Form filling agent completed successfully")
        logger.end_timer()
        
    except Exception as e:
        agent_tracker.log_action(request_id, "❌ Background form submission failed", str(e))
        logger.error(f"Background form submission failed: {e}")

@router.post("/submit-form", response_model=FormSubmissionResponse)
async def submit_form(request: FormSubmissionRequest, background_tasks: BackgroundTasks):
    """Submit form - returns immediately, processes in background"""
    # Generate unique request ID
    request_id = str(uuid.uuid4())[:8]
    
    # Create tracking file
    agent_tracker.create_request_file(request_id)
    agent_tracker.log_action(request_id, "📋 Request received", f"Account ID: {request.account_id or 'default'}")
    
    # Add form submission to background tasks
    background_tasks.add_task(process_form_submission_background, request, request_id)
    
    return FormSubmissionResponse(
        success=True,
        message="Form submission started in background",
        data={"status": "processing", "request_id": request_id}
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Humana Form Filling Agent"}
