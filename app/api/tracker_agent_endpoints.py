from fastapi import APIRouter, BackgroundTasks
import uuid
from app.schemas.tracker_agent import TrackerAgentRequest, TrackerAgentResponse
from app.services.tracker_agent import run_tracker_agent
from app.utils.agent_tracker import agent_tracker

router = APIRouter()

# Store active tracking tasks
active_tracking_tasks = {}

async def process_tracker_agent_background(request: TrackerAgentRequest, request_id: str):
    """Background task for tracker agent processing"""
    try:
        active_tracking_tasks[request_id] = {"status": "running", "started_at": "now"}
        agent_tracker.log_action(request_id, "🔄 Background task started")
        
        await run_tracker_agent(request_id, request)
        
        active_tracking_tasks[request_id] = {"status": "completed", "completed_at": "now"}
        agent_tracker.log_action(request_id, "✅ Background task completed successfully")
        
    except Exception as e:
        active_tracking_tasks[request_id] = {"status": "failed", "error": str(e), "failed_at": "now"}
        agent_tracker.log_action(request_id, f"❌ Background task failed: {str(e)}")
        
    finally:
        # Clean up completed tasks
        if request_id in active_tracking_tasks:
            del active_tracking_tasks[request_id]
            agent_tracker.log_action(request_id, "🧹 Background task cleaned up")

@router.post("/start-tracking", response_model=TrackerAgentResponse)
async def start_tracking(request: TrackerAgentRequest, background_tasks: BackgroundTasks):
    """Start Tracker Agent - returns immediately, processes in background"""
    # Generate unique request ID
    request_id = str(uuid.uuid4())[:8]
    
    # Create tracking file
    agent_tracker.create_request_file(request_id)
    agent_tracker.log_action(request_id, "📋 Tracker Agent request received")
    
    # Add tracker agent to background tasks
    background_tasks.add_task(process_tracker_agent_background, request, request_id)
    
    # Use custom values if provided, otherwise use defaults
    tracking_id = request.custom_tracking_id or "PA-14091005229"
    interval = request.custom_interval or 10
    
    return TrackerAgentResponse(
        success=True,
        message="Tracker Agent has started",
        data={
            "status": "tracking",
            "tracking_id": tracking_id,
            "interval_seconds": interval,
            "request_id": request_id
        }
    )

@router.get("/status/{request_id}")
async def get_tracking_status(request_id: str):
    """Get the status of a tracking task"""
    if request_id in active_tracking_tasks:
        return active_tracking_tasks[request_id]
    else:
        return {"status": "not_found", "message": "Request ID not found or task completed"}

@router.get("/active-tasks")
async def get_active_tracking_tasks():
    """Get all active tracking tasks"""
    return {
        "active_tasks": active_tracking_tasks,
        "count": len(active_tracking_tasks)
    }
