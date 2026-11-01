from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import time
import uuid

from models.registry import AI_FUNCTIONS


app = FastAPI(
    title="Serverless AI Inference Execution Kernel",
    description="Application-level OS kernel for fast AI inference execution",
    version="1.0.0"
)


class InferenceRequest(BaseModel):
    function: str
    input: Any


class InferenceResponse(BaseModel):
    execution_id: str
    function: str
    result: Any
    execution_time_ms: float
    status: str


@app.get("/")
def root():
    return {
        "system": "Serverless AI Inference Execution Kernel",
        "status": "running",
        "available_functions": list(AI_FUNCTIONS.keys())
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/inference", response_model=InferenceResponse)
def inference(request: InferenceRequest):

    execution_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    ai_function = AI_FUNCTIONS.get(request.function)

    if ai_function is None:
        return {
            "execution_id": execution_id,
            "function": request.function,
            "result": f"Function '{request.function}' not found",
            "execution_time_ms": 0,
            "status": "error"
        }

    result = ai_function(request.input)

    execution_time = (time.perf_counter() - start_time) * 1000

    return {
        "execution_id": execution_id,
        "function": request.function,
        "result": result,
        "execution_time_ms": round(execution_time, 3),
        "status": "completed"
    }
