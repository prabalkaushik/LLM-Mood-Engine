# Affective Subcortical Engine & Episodic Cognitive Middleware (Phase 1)

An MCP (Model Context Protocol) server that gives downstream LLMs a simulated physiological/emotional state (arousal, valence, energy, allostatic load) and an episodic vector memory.

## Runbook

```bash
# 1. Clone repository and start local infrastructure
git clone <repo_url> && cd affective-mcp-engine
docker compose up -d

# 2. Setup virtual environment & dependencies
python3 -m venv venv
source venv/bin/activate
pip install -e .

# 3. Seed foundational episodic memory bank
python scripts/seed_memories.py

# 4. Execute test suite
pytest -v tests/

# 5. Launch MCP Inspector for interactive protocol verification
./scripts/run_inspector.sh
```
