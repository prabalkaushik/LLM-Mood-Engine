import pytest
import random
from core.state_engine import _ensure_baseline, tick_homeostasis, apply_environmental_shock, InteroceptiveState

def test_ensure_baseline():
    state = _ensure_baseline(None)
    assert state.somatic_arousal == 0.15
    assert state.valence == 0.10
    assert state.energy_reserve == 1.00
    assert state.allostatic_load == 0.05
    # Default elasticity is 0.15 to ensure decay passes AC03
    assert state.elasticity == 0.15

def test_bounds_ac01():
    """AC01: Deterministic bounds - 10,000 randomized perturbations."""
    for _ in range(10000):
        S = random.random()
        U = random.random()
        C = random.random()
        
        state = InteroceptiveState(
            somatic_arousal=random.random(),
            valence=random.uniform(-1, 1),
            energy_reserve=random.random(),
            allostatic_load=random.random(),
            elasticity=0.15
        )
        
        new_state = apply_environmental_shock(state, S, U, C)
        assert 0.0 <= new_state.somatic_arousal <= 1.0
        assert -1.0 <= new_state.valence <= 1.0
        assert 0.0 <= new_state.energy_reserve <= 1.0
        assert 0.0 <= new_state.allostatic_load <= 1.0

def test_decay_ac03():
    """AC03: +300s post-shock reduces arousal >=50% toward baseline."""
    # Start with a high arousal state (e.g. max 1.0)
    state = InteroceptiveState(
        somatic_arousal=1.0, 
        valence=-1.0, 
        energy_reserve=1.0, 
        allostatic_load=1.0, 
        elasticity=0.15
    )
    
    new_state = tick_homeostasis(state, 300.0)
    
    A_base = 0.15
    initial_delta = 1.0 - A_base
    final_delta = new_state.somatic_arousal - A_base
    
    # Must reduce by at least 50%
    assert final_delta <= initial_delta * 0.5
