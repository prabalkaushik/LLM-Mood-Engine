import pytest
import json
from mcp_server.server import appraise_and_perturb, consolidate_experience, tick_metabolic_decay, read_interoception

def test_e2e_flow():
    # 1. Baseline check
    state_json = read_interoception()
    state = json.loads(state_json)
    assert state["somatic_arousal"] == 0.15
    
    # 2. Trigger & Shock
    trigger = "Production database deleted accidentally."
    res_json = appraise_and_perturb(trigger, base_severity=0.9, social_context="high_stakes")
    res = json.loads(res_json)
    
    appraisal = res["appraisal"]
    assert "severity" in appraisal
    
    telemetry = res["telemetry"]
    # arousal should spike
    assert telemetry["somatic_arousal"] > 0.15
    
    # 3. Consolidate experience
    cons_res = consolidate_experience(
        memory_id="mem_e2e_001", 
        trigger_event=trigger, 
        life_stage="adulthood", 
        constructed_concept="db_panic", 
        strategy_used="restore_backup", 
        orchestrator_feedback="successful", 
        reward_score=0.5, 
        resolved_successfully=True
    )
    assert "consolidated" in cons_res
    
    # 4. Tick decay
    tick_metabolic_decay(300.0)
    
    # 5. Check decay
    state2_json = read_interoception()
    state2 = json.loads(state2_json)
    assert state2["somatic_arousal"] < telemetry["somatic_arousal"]
