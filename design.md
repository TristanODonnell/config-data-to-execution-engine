# Config-Driven Data → ML Execution Engine — v1 Design

**Status:** Design (v1)  
**Scope:** Local-only, single-process, batch execution. YAML configs, filesystem artifacts, JSON run state.

---

## 1) One-Sentence Description

A **deterministic, config-driven DAG execution engine** that compiles a declarative pipeline specification into a validated execution plan and executes it synchronously with per-step retries, artifact tracking, and structured run state persistence.

---

## 2) Architectural Framing

This system is a:

- **Batch workflow engine**
- **Compile-then-execute runtime**
- **DAG-based task orchestration system**
- **Artifact-aware execution engine**

It is intentionally scoped as a **local, single-process runtime** to isolate core orchestration mechanics without introducing distributed complexity.

---

## 3) Locked Decisions (v1)

### Execution Model

- **Execution:** synchronous, single-process
- **Execution order:** topological order derived from validated DAG
- **Parallelism:** explicitly excluded (v1)
- **Scheduling:** not supported (no cron/interval triggers)

### Storage & State

- **Artifacts:** local filesystem only
- **Run state:** single JSON manifest per run (`run_manifest.json`)
- **Logs + metrics:** per-step files inside run directory

### Configuration

- **Pipeline definition:** YAML
- **Validation:** static schema + dependency validation
- **Extensibility:** Step Registry (`type` → implementation binding)

### Retry Semantics

- **Per-step retry policy**
- Fixed backoff (`backoff_seconds`)
- Pipeline halts if a step exceeds retry budget
- No exponential backoff (v1)

---

## 4) High-Level System Architecture

```text
pipeline.yaml
  ↓
[ Config Parser ]
  ↓
[ Pipeline Compiler ]
  → validates schema
  → validates dependencies
  → detects cycles
  → builds DAG
  → produces execution plan (topological order)
  ↓
[ Execution Engine ]
  → resolves runnable steps
  → executes steps deterministically
  → applies retry semantics
  → writes artifacts + logs + metrics
  → persists structured state to run_manifest.json
  ↓
runs/<run_id>/
  ├─ run_manifest.json
  └─ steps/<step_id>/
       ├─ step_log.txt
       ├─ step_metrics.json
       └─ artifacts/
```
## 5) Compile vs Runtime Phases

### Compile Phase (Static)

**Input:** YAML config  
**Output:** Validated DAG + execution plan  

**Responsibilities:**

- Schema validation  
- Duplicate ID detection  
- Unknown dependency detection  
- Cycle detection  
- DAG construction  
- Topological sorting  

This phase fails fast before any execution occurs.

---

### Runtime Phase (Dynamic)

**Input:** Execution plan  
**Output:** Artifacts + `run_manifest.json`  

**Responsibilities:**

- Step state transitions  
- Retry handling  
- Failure propagation  
- Artifact registration  
- Metrics + log emission  
- State persistence  

---

## 6) Core Domain Definitions

### Pipeline

A **pipeline** is a declarative workflow specification composed of:

- Named steps  
- Directed dependency edges (DAG)  
- Optional default execution policies  

A pipeline describes **what should happen**, not **how it is executed**.

---

### Step

A **step** is a single node in the DAG and represents an atomic unit of work.

Each step contains:

- `id`: unique identifier  
- `type`: implementation selector (Step Registry binding)  
- `depends_on`: upstream step IDs (optional)  
- `params`: step-specific configuration  
- optional retry overrides  

A step implementation is responsible only for business logic, not orchestration logic.

---

### Execution Plan

An **execution plan** is a topologically sorted ordering of steps that respects dependency constraints.

This plan is derived during compilation and remains fixed during execution.

---

### Execution State

Execution state is the structured record of a pipeline run.

Stored in `run_manifest.json`, it includes:

- Per-step status:
  - `PENDING`
  - `RUNNING`
  - `SUCCESS`
  - `FAILED`
  - `SKIPPED`
- Attempt counts  
- Timestamps  
- Error metadata  
- Registered artifacts  

State transitions form a simple task state machine.

---

### Artifact

An **artifact** is a persistent output produced by a step.

Stored under:


Tracked metadata includes:

- `name`
- `path`
- `kind`
- producing step ID  

Artifacts enable lineage and reproducibility.

---

## 7) Determinism & Reproducibility (v1 Guarantees)

The engine guarantees:

- Deterministic execution order  
- Explicit dependency resolution  
- Fail-fast compile validation  
- Structured state persistence  
- Artifact traceability  

It does **not** guarantee:

- Distributed consistency  
- Parallel execution ordering  
- Remote storage durability  
- Fault-tolerant recovery across machines  

---

## 8) Non-Goals (v1)

This project is explicitly **not**:

- A UI platform  
- A cloud-native system  
- A scheduler  
- A distributed worker system  
- A streaming engine  
- An online inference system  
- A full Airflow/dbt/MLflow replacement  

It is a **core orchestration runtime**.

---

## 9) YAML Configuration Shape (v1)

### Minimal Example

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
