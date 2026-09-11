# Agentic Environment & Evaluation Benchmark

A production-style sandbox environment for training and benchmarking autonomous AI agents on complex, multi-step enterprise workflows across simulated SaaS APIs (Linear/Slack).

## Architecture Overview

```text
               +----------------------------------+
               |         AI Agent / LLM           |
               +----------------------------------+
                                |
                                | Executes Tool Calls
                                v
               +----------------------------------+
               |    environment/connector.py      |
               | (Translates function schemas to  |
               |     HTTP endpoints)              |
               +----------------------------------+
                                |
                                | HTTP REST Calls
                                v
               +----------------------------------+
               |     mock_saas/ (FastAPI + DB)    |
               | - /api/v1/issues                 |
               | - /admin/reset                   |
               +----------------------------------+
                                ^
                                | Validates State Delta
               +----------------------------------+
               |        eval/evaluator.py         |
               |  (Determines Task Pass/Fail)     |
               +----------------------------------+
```

## Quickstart Guide

1. **Spin up the Mock SaaS Server:**
   ```bash
   cd mock_saas
   docker compose up --build -d
   ```

2. **Run an Agent Benchmark Task:**
   ```bash
   # From root directory
   python -m eval.evaluator --task tasks/task_001_triage_bug.json
   ```
