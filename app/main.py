from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import time
import uuid

from models.registry import AI_FUNCTIONS
from models.execution import ExecutionKernel

execution_kernel = ExecutionKernel(AI_FUNCTIONS)


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
    return execution_kernel.execute(request.function, request.input)
