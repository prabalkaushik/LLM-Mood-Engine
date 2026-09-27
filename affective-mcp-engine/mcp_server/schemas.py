from pydantic import BaseModel, Field

class AppraisePerturbInput(BaseModel):
    trigger_event: str
    base_severity: float = Field(ge=0.0, le=1.0)
    social_context: str = "neutral"
    top_k_priors: int = 2

class ConsolidateExperienceInput(BaseModel):
    memory_id: str
    trigger_event: str
    life_stage: str
    constructed_concept: str
    strategy_used: str
    orchestrator_feedback: str
    reward_score: float = Field(ge=-1.0, le=1.0)
    resolved_successfully: bool

class TickDecayInput(BaseModel):
    elapsed_seconds: float = Field(ge=0.0)
