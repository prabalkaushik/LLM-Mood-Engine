import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.appraisal_engine import MemoryStore

def seed():
    store = MemoryStore()
    
    memories = [
        {
            "memory_id": "mem_child_001",
            "trigger_text": "Unexpectedly encountering a large dog barking loudly.",
            "life_stage": "childhood",
            "constructed_concept": "startle_freeze",
            "strategy_used": "hide_behind_caregiver",
            "orchestrator_feedback": "threat_averted",
            "reward_score": 0.4,
            "delta_allostasis": 0.10,
            "resolved_successfully": True,
            "timestamp": time.time() - 2000000
        },
        {
            "memory_id": "mem_child_002",
            "trigger_text": "Failing a simple task and being publicly laughed at.",
            "life_stage": "childhood",
            "constructed_concept": "social_withdrawal",
            "strategy_used": "avoidance_and_silence",
            "orchestrator_feedback": "shame_internalized",
            "reward_score": -0.6,
            "delta_allostasis": 0.25,
            "resolved_successfully": False,
            "timestamp": time.time() - 1500000
        },
        {
            "memory_id": "mem_adol_019",
            "trigger_text": "Executive sponsor abruptly demands deprecation of core microservices.",
            "life_stage": "adolescence",
            "constructed_concept": "defensive_vigilance",
            "strategy_used": "audit_trail_isolation_and_benchmarking",
            "orchestrator_feedback": "de_escalated_and_retained_ownership",
            "reward_score": 0.85,
            "delta_allostasis": -0.15,
            "resolved_successfully": True,
            "timestamp": time.time() - 500000
        },
        {
            "memory_id": "mem_early_adult_042",
            "trigger_text": "System outage during peak traffic caused by my own code deploy.",
            "life_stage": "early_adulthood",
            "constructed_concept": "acute_panic_mitigation",
            "strategy_used": "immediate_rollback_and_blameless_postmortem",
            "orchestrator_feedback": "system_restored_trust_maintained",
            "reward_score": 0.70,
            "delta_allostasis": 0.05,
            "resolved_successfully": True,
            "timestamp": time.time() - 100000
        },
        {
            "memory_id": "mem_adult_099",
            "trigger_text": "Navigating a complex architectural disagreement between two senior engineers.",
            "life_stage": "adulthood",
            "constructed_concept": "diplomatic_mediation",
            "strategy_used": "steelmanning_both_sides_and_finding_compromise",
            "orchestrator_feedback": "consensus_reached_and_architecture_approved",
            "reward_score": 0.90,
            "delta_allostasis": -0.10,
            "resolved_successfully": True,
            "timestamp": time.time() - 10000
        }
    ]
    
    for m in memories:
        store.record_memory(m)
        
    print(f"Successfully seeded {len(memories)} memories into Qdrant collection '{store.collection_name}'.")

if __name__ == "__main__":
    seed()
