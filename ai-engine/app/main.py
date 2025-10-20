"""
Stratomai Agents - AI Engine
FastAPI microservice for AI processing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Stratomai AI Engine",
    description="AI Processing Engine for Stratomai Agents Platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELS
# ============================================================

class InstructionInput(BaseModel):
    instruction: str
    user_id: str
    agent_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ParsedIntent(BaseModel):
    action: str
    entities: Dict[str, Any]
    confidence: float
    capabilities_required: List[str]
    suggested_agent: Optional[str] = None

class ExecutionStep(BaseModel):
    step_index: int
    step_name: str
    step_type: str
    action: str
    parameters: Dict[str, Any]
    dependencies: List[int] = []

class ExecutionPlan(BaseModel):
    task_id: str
    steps: List[ExecutionStep]
    total_steps: int
    estimated_duration_ms: int
    requires_approval: bool

class AgentSuggestion(BaseModel):
    agent_id: str
    agent_name: str
    agent_role: str
    confidence: float
    reasoning: str

# ============================================================
# ROUTES
# ============================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Stratomai AI Engine",
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
    }

@app.post("/ai/parse-instruction", response_model=ParsedIntent)
async def parse_instruction(input: InstructionInput):
    """
    Parse natural language instruction into structured intent

    This endpoint uses LLM to analyze the user's instruction and extract:
    - The main action to perform
    - Entities (emails, dates, names, etc.)
    - Required capabilities
    - Suggested agent
    """
    try:
        # TODO: Implement actual LLM parsing
        # For now, return mock data

        # Simulate intent parsing
        parsed = ParsedIntent(
            action="send_email",
            entities={
                "recipient": "john@example.com",
                "subject": "Meeting Follow-up",
                "priority": "high"
            },
            confidence=0.92,
            capabilities_required=["email"],
            suggested_agent="email_assistant"
        )

        return parsed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/generate-plan", response_model=ExecutionPlan)
async def generate_execution_plan(input: InstructionInput):
    """
    Generate detailed execution plan from instruction

    Breaks down the instruction into concrete steps that can be executed
    by the workflow engine (n8n).
    """
    try:
        # TODO: Implement actual plan generation with LangChain
        # For now, return mock plan

        plan = ExecutionPlan(
            task_id="mock-task-id",
            steps=[
                ExecutionStep(
                    step_index=0,
                    step_name="Fetch email template",
                    step_type="data_retrieval",
                    action="get_template",
                    parameters={"template_id": "meeting_followup"},
                    dependencies=[]
                ),
                ExecutionStep(
                    step_index=1,
                    step_name="Compose email",
                    step_type="data_transform",
                    action="compose_email",
                    parameters={
                        "recipient": "john@example.com",
                        "subject": "Meeting Follow-up"
                    },
                    dependencies=[0]
                ),
                ExecutionStep(
                    step_index=2,
                    step_name="Send email",
                    step_type="api_call",
                    action="send_email",
                    parameters={"provider": "gmail"},
                    dependencies=[1]
                )
            ],
            total_steps=3,
            estimated_duration_ms=5000,
            requires_approval=False
        )

        return plan

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/classify-intent")
async def classify_intent(input: InstructionInput):
    """
    Classify the intent of the instruction

    Returns the category and subcategory of the task
    """
    try:
        # TODO: Implement actual classification
        return {
            "category": "communication",
            "subcategory": "email",
            "complexity": "medium",
            "confidence": 0.89
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/suggest-agent", response_model=List[AgentSuggestion])
async def suggest_agent(input: InstructionInput):
    """
    Suggest the best agent(s) for the given instruction

    Analyzes the instruction and returns ranked agent suggestions
    """
    try:
        # TODO: Implement actual agent matching
        suggestions = [
            AgentSuggestion(
                agent_id="email_assistant",
                agent_name="Email Assistant",
                agent_role="email_assistant",
                confidence=0.95,
                reasoning="La tarea requiere envío de emails y el agente está especializado en comunicación por email"
            )
        ]

        return suggestions

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/extract-entities")
async def extract_entities(input: InstructionInput):
    """
    Extract entities from instruction (dates, emails, names, etc.)
    """
    try:
        # TODO: Implement NER with LangChain
        return {
            "entities": {
                "dates": [],
                "emails": ["john@example.com"],
                "names": ["John"],
                "locations": [],
                "organizations": []
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# STARTUP/SHUTDOWN
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 AI Engine starting up...")
    # TODO: Initialize LLM clients, Redis connection, etc.

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 AI Engine shutting down...")
    # TODO: Close connections, cleanup resources

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
