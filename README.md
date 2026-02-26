# config-data-to-execution-engine

![Status](https://img.shields.io/badge/status-active--development-blue)

This project is a local, single-process DAG execution engine built in Python to explore pipeline compilation, orchestration, and run-state persistence.

---

## Why I Built This

After building larger data-heavy systems, I wanted to step back and understand the core mechanics behind industry data tools:

- How pipeline specs become executable DAGs
- How step dependencies are validated and ordered
- How retries and failure states are handled
- How run state and artifacts are persisted
- How logging and warehousing layers attach to orchestration

Rather than using an existing framework, I’m building the layers myself:

1. **Execution engine (DAG compiler + runner)** — implemented
2. **Structured logging layer** — next
3. **Warehouse / materialization layer** — next

The objective is to internalize data engineering fundamentals by building them.

---

## Current Scope (v1)

- YAML-based pipeline specifications
- Step registry + typed step execution
- DAG compilation + topological sort
- Per-step retries and backoff
- Filesystem-backed run state
- Artifact directories per step

Execution model:
- Local only
- Single process
- Batch execution

---

## Example

Run a pipeline:

```bash
    # python -m engine.cli configs/config_v1.yaml
    # python -m engine.cli configs/retry_test.yaml
    # --debug - debugging prints
    # --plan
        # run without --plan for full execution logic