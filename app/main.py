from fastapi import FastAPI
from app.api.form_submission_endpoints import router

app = FastAPI(title="Humana Form Filling Agent API", version="1.0.0")

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Humana Form Filling Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
