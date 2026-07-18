# Sales Report — Multi-Paradigm Code Showcase

**Purpose:** Demonstrates how the same business logic (a simple sales performance report)
can be implemented using multiple programming paradigms and architectural styles in Python.

---

## Project Overview

All implementations compute the same core metrics from `sales_data.csv`:

- Number of customers
- Average order value (pre-tax)
- Percentage of returns
- Total sales in period (pre-tax)

Each version differs only in *structure* and *paradigm emphasis*.

| Paradigm | File | Highlights |
|-----------|------|------------|
| Procedural / Baseline | `messy_report.py` | Imperative style, easy to follow but not modular |
| Object-Oriented (SOLID) | Legacy: `class_based_report.py`<br>Enhanced: `class_based_report_v2.py` | Classes and interfaces; SRP and OCP applied with improved logging/robustness |
| Functional | Legacy: `functional_report.py`<br>Enhanced: `functional_report_v2.py` | Pure transformations with v2 adding structured logging and stronger error handling |
| Declarative Pipeline | `declarative_report.py` | Type-checked pipelines using Pandera |
| Config-Driven | `config_report.py` | YAML configuration defines logic dynamically |
| Asynchronous | `async_report.py` | Concurrent metric computation and async I/O |
| Async Streaming (No Pandas) | `async_no_pandas_report.py` | True non-blocking CSV streaming with aiofiles |
| Dataflow / DAG | `report_dataflow.py` | Declarative dependency graph with explicit dataflow |
| Actor Model | `report_actor_model.py` | Cooperative message-passing actors with isolated state |
| Reactive | `reactive_report.py` | RxPY stream-based reporting |
| Logic / Relational | `logic_report.py` | Relational facts and symbolic reasoning via Kanren |

> The legacy functional and class-based versions match the walkthrough in the video. The `_v2` editions layer in richer logging, error handling, and filesystem conventions while preserving the same outputs.

---

## Usage

### 1. Setup Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Install it if you have not already, then run:

```bash
uv sync
```

### 2. Run Examples

#### Option A — Helper Script

From this directory you can execute one or more implementations with the helper script:

```bash
./run_reports.sh --list          # view available keys
./run_reports.sh --run functional --run logic
./run_reports.sh --run-all
```

The script uses `uv run` automatically when `uv` is installed (recommended). Use `--dry-run` to preview the commands without executing them.

#### Option B — Manual Commands

Use `uv run` to execute any of the implementations inside the managed environment:

```bash
uv run python logic_report.py
uv run python functional_report.py
uv run python functional_report_v2.py
uv run python async_report.py
uv run python async_no_pandas_report.py
uv run python report_dataflow.py
uv run python report_actor_model.py
uv run python class_based_report.py
uv run python class_based_report_v2.py
uv run python reactive_report.py
# etc.
```

### 3. Validate Outputs

After running one or more implementations, verify the generated JSON payloads agree:

```bash
uv run python verify_reports.py          # compare every file to the first baseline
uv run python verify_reports.py --verbose
uv run python verify_reports.py --baseline sales_report.json
```

The script checks for consistent keys and values (within a configurable tolerance) across every report implementation. A non-zero exit code indicates a mismatch.

## Educational Goal

This project illustrates how:

- The same logic can map into multiple thought models (OOP, FP, Async, Logic).
- Paradigm choice affects extensibility, readability, and reasoning complexity.
- Abstraction boundaries (metrics, config, I/O) remain constant across paradigms.
