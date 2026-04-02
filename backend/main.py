from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Anti-Ragging AI Backend Running"}

from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection
import uuid

app = FastAPI()

# ✅ This fixes Swagger UI input
class Complaint(BaseModel):
    description: str


def generate_tracking_id():
    return str(uuid.uuid4())[:8]


@app.post("/report")
def report_complaint(data: Complaint):
    description = data.description

    tracking_id = generate_tracking_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (tracking_id, description)
        VALUES (%s, %s)
    """, (tracking_id, description))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Complaint submitted successfully",
        "tracking_id": tracking_id
    }


