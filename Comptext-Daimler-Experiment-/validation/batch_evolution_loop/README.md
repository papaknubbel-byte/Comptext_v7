# Batch Evolution Loop (Validation Module)

## Purpose
Deterministic batch-based evolution loop for code optimization. This module enables automated, reproducible search for optimal code patches by iteratively mutating, evaluating, and ranking candidate solutions.

## Architecture
The system follows a modular pipeline architecture:
1. **Generator**: Produces deterministic mutations (candidates) based on a base system state and seed.
2. **Orchestrator**: Manages the full lifecycle of a batch execution.
3. **Scorer**: Calculates a multi-metric score (Correctness, Performance, Regression Risk).
4. **Memory**: Provides persistent storage for experiment history and best candidates in JSONL format.
5. **Runner**: The execution entry point that connects the loop to the evaluation backend.

## How to Run
Execute the loop from the repository root:
```bash
python -m validation.batch_evolution_loop.runner
```

## Scoring System
The scoring function is a weighted linear combination of three core metrics:
- **Correctness (55%)**: Functional accuracy and test pass rate.
- **Performance (30%)**: Latency and resource utilization.
- **Regression Risk (-15%)**: Potential negative impact on existing features.

Formula: `score = 0.55 * correctness + 0.30 * performance - 0.15 * regression_risk`

## Connection to Autoresearch Sandbox
This module integrates with the `/validation/autoresearch_sandbox/` as its evaluation backend. The Sandbox provides the `run_experiment(patch)` interface, which returns the raw metrics consumed by the Scorer. In the current implementation, this interface is mocked for local determinism but is designed to be swapped with a real sandbox runner.

## Future Extension Path
- **MCP Integration**: Expose the Evolution Loop as an MCP tool for agentic orchestration.
- **Rust CI Gate**: Implement high-performance validation gates using Rust for sub-millisecond evaluation cycles.
- **Distributed Evaluation**: Scale batch evaluation across multiple isolated sandbox environments.
