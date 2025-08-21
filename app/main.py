from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.form_submission_endpoints import router as form_router
from app.api.tracker_agent_endpoints import router as tracker_router

app = FastAPI(title="Humana Form Filling Agent API", version="1.0.0")

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(form_router, prefix="/api/v1/form")
app.include_router(tracker_router, prefix="/api/v1/tracker")

@app.get("/")
async def root():
    return {"message": "Humana Form Filling Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
