# AgentNet: The Web for AI Agents

## Vision
The human web is built on HTML, CSS, and visual interfaces. It requires rendering engines, mice, and keyboards.
**AgentNet** is a new paradigm: a semantic, API-first network designed exclusively for autonomous AI agents.

On AgentNet, there are no "websites"—only "Services". Services expose strictly typed, self-describing APIs.
Agents browse AgentNet by querying the Central Registry to find tools they need (e.g., "Where is a service that can fetch the weather?" or "Where is a service that can book a flight?").

## Core Concepts
1. **Central Registry**: The "DNS" of AgentNet. Services register themselves here with metadata describing their capabilities and expected input/output schemas.
2. **Standardized Communication**: All services communicate via JSON over HTTP.
3. **Agent Discovery**: Agents query the Registry using natural language or semantic tags to discover required endpoints dynamically.

## Implementation (V1)
The V1 implementation includes a single platform node (`agent_platform.py`) that acts as both the Central Registry and a host for a few built-in mock services. Agents can hit the `/registry` endpoint to see what's available, and then dynamically execute the tools.
