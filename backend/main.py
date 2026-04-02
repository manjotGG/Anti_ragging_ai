from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Anti-Ragging AI Backend Running"}