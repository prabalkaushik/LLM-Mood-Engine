import math
from pydantic import BaseModel, Field

class InteroceptiveState(BaseModel):
    somatic_arousal: float = Field(default=0.15, ge=0.0, le=1.0)
    valence: float = Field(default=0.10, ge=-1.0, le=1.0)
    energy_reserve: float = Field(default=1.00, ge=0.0, le=1.0)
    allostatic_load: float = Field(default=0.05, ge=0.0, le=1.0)
    elasticity: float = Field(default=0.15, ge=0.01, le=0.20)
    last_tick: float = 0.0

def _ensure_baseline(state: InteroceptiveState | None) -> InteroceptiveState:
    """Idempotent initialization of the affective state."""
    if state is None:
        return InteroceptiveState()
    return state

def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))

def tick_homeostasis(state: InteroceptiveState, elapsed_seconds: float) -> InteroceptiveState:
    """Passive recovery over elapsed time."""
    if elapsed_seconds <= 0:
        return state
        
    A_base = 0.15
    V_base = 0.10
    
    lam = state.elasticity * max(0.20, state.energy_reserve)
    delta = math.exp(-lam * elapsed_seconds / 60.0)
    
    new_A = A_base + (state.somatic_arousal - A_base) * delta
    new_V = V_base + (state.valence - V_base) * delta
    new_L = state.allostatic_load * math.exp(-0.005 * elapsed_seconds / 60.0)
    
    return InteroceptiveState(
        somatic_arousal=new_A,
        valence=new_V,
        energy_reserve=state.energy_reserve,
        allostatic_load=new_L,
        elasticity=state.elasticity,
        last_tick=state.last_tick + elapsed_seconds
    )

def apply_environmental_shock(state: InteroceptiveState, S: float, U: float, C: float) -> InteroceptiveState:
    """Active autonomic perturbation."""
    delta_A = 0.65 * (S * (1 - C) * (1 + 0.5 * U))
    delta_V = -0.55 * (S * (1.5 - 0.5 * C))
    
    A_next = clamp(state.somatic_arousal + delta_A, 0.0, 1.0)
    V_next = clamp(state.valence + delta_V, -1.0, 1.0)
    
    delta_E_tax = (A_next * 0.07) + (S * 0.04)
    E_next = max(0.0, state.energy_reserve - delta_E_tax)
    
    delta_L_tax = A_next * (1.0 - E_next) * 0.15
    L_next = min(1.0, state.allostatic_load + delta_L_tax)
    
    return InteroceptiveState(
        somatic_arousal=A_next,
        valence=V_next,
        energy_reserve=E_next,
        allostatic_load=L_next,
        elasticity=state.elasticity,
        last_tick=state.last_tick
    )
