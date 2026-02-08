# Config-Driven Data to ML Execution Engine — v1 Design

Status: Design (v1)  
Scope: Local-only, synchronous execution, YAML configs, filesystem artifacts, JSON run state

---

## 1) One-sentence description

A **YAML-configured execution engine** that parses a pipeline spec, compiles it into a validated DAG, then **executes steps synchronously** with **per-step retries**, writing **artifacts to the local filesystem** and recording full **run + step state** in a `run_manifest.json`.

---

## 2) Locked decisions (v1)

### Execution & environment
- **Execution:** synchronous, single-process
- **Artifacts:** local filesystem only
- **State storage:** single JSON file per run (`run_manifest.json`)
- **Configs:** YAML
- **Extensibility:** Step Registry (string `type` → implementation)

### Retry semantics (B1)
- **Per-step retries** with **fixed backoff**
- Stop the pipeline if a step exceeds its retry budget

---

## 3) Mental model

Building the **conveyor + manager** (engine), not the **machines** (step logic).

```text
pipeline.yaml
  ↓
[ Config Parser ]
  ↓
[ Pipeline Compiler ]
  → validates schema
  → builds DAG
  ↓
[ Execution Engine ]
  → executes steps in topological order
  → handles per-step retries + fixed backoff
  → writes artifacts + logs + metrics
  → tracks execution state in run_manifest.json
  ↓
runs/<run_id>/
  ├─ run_manifest.json
  └─ steps/<step_id>/
       ├─ step_log.txt
       ├─ step_metrics.json
       └─ artifacts/...

--- 

## 4) Definitions (v1)

### Pipeline
A **pipeline** is a named workflow defined in YAML consisting of:
- a list of **steps**
- dependency edges between steps (a DAG)
- optional defaults (e.g., retries/backoff)

### Step
A **step** is a single unit of work (a node in the DAG).
Each step has:
- `id`: unique identifier
- `type`: selects an implementation from the Step Registry
- `depends_on`: upstream step ids that must complete first (optional)
- `params`: step-specific configuration
- optional retry overrides: `retries`, `backoff_seconds`

### Execution state
**Execution state** is the structured record of what happened during a run:
- per-step status (PENDING/RUNNING/SUCCESS/FAILED/SKIPPED)
- attempts, timestamps, and errors
- produced artifacts and their paths
State is stored in a single JSON file: `run_manifest.json`.

### Artifact
An **artifact** is an output produced by a step and saved to disk under:
`runs/<run_id>/steps/<step_id>/artifacts/`
Artifacts are tracked in the manifest with minimal metadata:
- `name`, `path`, `kind`

---

## 5) Non-goals (v1)

This project is **not**:
- a UI product
- a cloud/AWS demo
- a production SaaS
- a scheduler (cron/interval scheduling)
- a distributed or parallel execution system
- a streaming engine
- an online inference/serving system
- a full Airflow/dbt/MLflow replacement

---

## 6) YAML config shape (v1)

### Minimal example
```yaml
pipeline:
  name: example_pipeline
  defaults:
    retries: 2
    backoff_seconds: 2
  steps:
    - id: step_a
      type: write_file
      params:
        text: "hello"

    - id: step_b
      type: copy_file
      depends_on: [step_a]
      params:
        path: data/input.txt