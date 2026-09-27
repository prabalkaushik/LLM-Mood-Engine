import json
import time
import redis
from mcp.server.fastmcp import FastMCP
from core.state_engine import InteroceptiveState, _ensure_baseline, tick_homeostasis, apply_environmental_shock
from core.appraisal_engine import MemoryStore
from config.settings import settings
from mcp_server.schemas import AppraisePerturbInput, ConsolidateExperienceInput, TickDecayInput

mcp = FastMCP("Affective-Subcortical-Engine")

def get_redis_client():
    return redis.Redis.from_url(settings.redis_url, decode_responses=True, max_connections=10)

def load_state() -> InteroceptiveState:
    try:
        r = get_redis_client()
        key = f"agent:{settings.agent_id}:telemetry"
        data = r.hgetall(key)
        if not data:
            return _ensure_baseline(None)
        
        return InteroceptiveState(
            somatic_arousal=float(data.get("somatic_arousal", 0.15)),
            valence=float(data.get("valence", 0.10)),
            energy_reserve=float(data.get("energy_reserve", 1.00)),
            allostatic_load=float(data.get("allostatic_load", 0.05)),
            elasticity=float(data.get("elasticity", 0.15)),
            last_tick=float(data.get("last_tick", 0.0))
        )
    except redis.ConnectionError:
        # Graceful fallback for testing when redis is not available
        return _ensure_baseline(None)

def save_state(state: InteroceptiveState):
    try:
        r = get_redis_client()
        key = f"agent:{settings.agent_id}:telemetry"
        r.hset(key, mapping={
            "somatic_arousal": str(state.somatic_arousal),
            "valence": str(state.valence),
            "energy_reserve": str(state.energy_reserve),
            "allostatic_load": str(state.allostatic_load),
            "elasticity": str(state.elasticity),
            "last_tick": str(state.last_tick)
        })
    except redis.ConnectionError:
        pass

@mcp.resource("interoception://current")
def read_interoception() -> str:
    state = load_state()
    return json.dumps({
        "somatic_arousal": state.somatic_arousal,
        "valence": state.valence,
        "energy_reserve": state.energy_reserve,
        "allostatic_load": state.allostatic_load,
        "elasticity": state.elasticity,
        "timestamp": time.time()
    })

@mcp.resource("allostasis://summary")
def read_allostasis() -> str:
    state = load_state()
    burnout_risk = "low"
    if state.allostatic_load > 0.8:
        burnout_risk = "high"
    elif state.allostatic_load > 0.5:
        burnout_risk = "moderate"
        
    system_status = "nominal"
    if state.energy_reserve < 0.2:
        system_status = "depleted_operating_state"
    elif state.somatic_arousal > 0.8:
        system_status = "hyperaroused_operating_state"
    elif state.allostatic_load > 0.7:
        system_status = "strained_operating_state"
        
    return json.dumps({
        "allostatic_load": state.allostatic_load,
        "burnout_risk": burnout_risk,
        "recovery_elasticity": state.elasticity,
        "metabolic_fuel": state.energy_reserve,
        "system_status": system_status
    })

@mcp.tool()
def appraise_and_perturb(trigger_event: str, base_severity: float, social_context: str = "neutral", top_k_priors: int = 2) -> str:
    store = MemoryStore()
    appraisal = store.compute_appraisal(trigger_event, base_severity, 0.5, top_k=top_k_priors)
    
    state = load_state()
    new_state = apply_environmental_shock(state, appraisal["S"], appraisal["U"], appraisal["C"])
    save_state(new_state)
    
    return json.dumps({
        "appraisal": {
            "severity": appraisal["S"],
            "controllability": appraisal["C"],
            "unpredictability": appraisal["U"]
        },
        "telemetry": {
            "somatic_arousal": new_state.somatic_arousal,
            "valence": new_state.valence,
            "energy_reserve": new_state.energy_reserve,
            "allostatic_load": new_state.allostatic_load
        },
        "retrieved_priors": appraisal["priors"]
    })

@mcp.tool()
def consolidate_experience(memory_id: str, trigger_event: str, life_stage: str, constructed_concept: str, strategy_used: str, orchestrator_feedback: str, reward_score: float, resolved_successfully: bool) -> str:
    store = MemoryStore()
    
    delta_allostasis = -0.1 if resolved_successfully else 0.1
    
    payload = {
        "memory_id": memory_id,
        "trigger_text": trigger_event,
        "life_stage": life_stage,
        "constructed_concept": constructed_concept,
        "strategy_used": strategy_used,
        "orchestrator_feedback": orchestrator_feedback,
        "reward_score": reward_score,
        "delta_allostasis": delta_allostasis,
        "resolved_successfully": resolved_successfully,
        "timestamp": time.time()
    }
    store.record_memory(payload)
    return "Memory consolidated."

@mcp.tool()
def tick_metabolic_decay(elapsed_seconds: float) -> str:
    state = load_state()
    new_state = tick_homeostasis(state, elapsed_seconds)
    save_state(new_state)
    return "Decay applied."

@mcp.prompt()
def construct_affective_response() -> str:
    return f"""
<think>
1. Interoceptive assessment: Read interoception://current and allostasis://summary.
2. Historical credit assignment: Consider retrieved priors and their outcomes.
3. Situated conceptualization: Construct an ad-hoc affective concept suitable for this precise context and internal state.
4. Emergent strategy generation: Determine response urgency, risk tolerance, and tone based on energy reserve and allostatic load.
</think>
Respond in accordance with your determined internal state. Do not explicitly mention your internal telemetry values or terms like 'interoception' or 'allostatic load'. Let the state manifest purely through tone, syntax, and risk tolerance.
"""
