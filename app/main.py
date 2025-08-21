from fastapi import FastAPI
from app.api.form_submission_endpoints import router as form_router
from app.api.tracker_agent_endpoints import router as tracker_router

app = FastAPI(title="Humana Form Filling Agent API", version="1.0.0")

app.include_router(form_router, prefix="/api/v1/form")
app.include_router(tracker_router, prefix="/api/v1/tracker")

@app.get("/")
async def root():
    return {"message": "Humana Form Filling Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
