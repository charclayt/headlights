from fastapi import FastAPI

app = FastAPI(title="ML Service API")

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "ML service is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)