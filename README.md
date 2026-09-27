# LLM Mood Engine (Affective MCP)

## Overview
The **LLM Mood Engine** (Affective Subcortical Engine & Episodic Cognitive Middleware) introduces a paradigm shift in how artificial intelligence systems interact with users. Through the Model Context Protocol (MCP), it provisions downstream Large Language Models (LLMs) with a persistent, simulated physiological and emotional state, seamlessly integrating dynamic "moods" and episodic vector memory into the AI's cognitive loop.

## The Core Problem
Modern AI systems, despite their vast knowledge, are inherently stateless and emotionally flat. They process each prompt in a vacuum, lacking the biological and emotional continuity that defines human interaction. An AI doesn't get "tired" after a long conversation, nor does it carry over "enthusiasm" from a recent positive interaction. This results in interactions that, while intelligent, often feel robotic, generic, and disconnected from the user's emotional context.

## Use-Case Methodology: Designing AI with "Affective Continuity"

The LLM Mood Engine provides a highly effective methodology for adapting your current AI system to a specific use case by grounding its responses in an evolving internal state. Here's how it revolutionizes system design:

### 1. Physiological & Emotional Anchoring
The engine simulates core subcortical dimensions:
*   **Arousal & Valence:** Determines if the AI is excited, calm, frustrated, or happy.
*   **Energy Levels:** The AI can experience "fatigue," prompting it to provide more concise, direct answers when energy is low, or expansive, creative answers when energy is high.
*   **Allostatic Load:** Measures cumulative stress, allowing the AI to change its behavior over prolonged, complex interactions.

**Methodology Application:** Instead of hard-coding "personas," you map system events to physiological shifts. A customer support AI dealing with a complex, failing technical issue will experience higher allostatic load and shift to a highly focused, empathetic, and serious tone automatically.

### 2. Episodic Vector Memory
Instead of traditional semantic RAG (Retrieval-Augmented Generation) which simply retrieves "facts," this middleware leverages **episodic memory**. 

**Methodology Application:** The AI remembers *how* a past interaction felt. When retrieving a past conversation with a user, it retrieves the emotional valence associated with that event. This allows an AI companion to build genuine rapport, recalling not just what was said, but the shared sentiment of the experience.

### 3. Dynamic Context Provisioning via MCP
By acting as an MCP Server, the Mood Engine non-intrusively augments existing LLM workflows. 

**Methodology Application:** You do not need to retrain or fine-tune massive foundation models. The Mood Engine dynamically injects the current affective state and relevant episodic memories directly into the context window, making it a highly modular, plug-and-play solution to upgrade any existing LLM application.

## Ideal Use Cases

1.  **Next-Generation Virtual Companions:** Creating companions that develop complex emotional arcs, remember past interactions, and display evolving personalities based on how the user treats them.
2.  **Adaptive Customer Support:** Systems that detect user frustration, modulate their own internal state to project calm empathy, and prioritize resolution over generic scripts.
3.  **Dynamic Gaming NPCs:** Non-player characters with genuine physiological states, where a character might refuse to help the player if their "energy" is too low or their "valence" towards the player is negative due to past episodic memories.

## Getting Started

To explore the underlying engine and start the infrastructure (including Dockerized vector stores and state engines), please navigate to the `affective-mcp-engine` directory.

```bash
cd affective-mcp-engine
# Follow the runbook in affective-mcp-engine/README.md
```
