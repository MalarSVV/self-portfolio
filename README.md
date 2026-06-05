# LLM (Text-to-SQL Platform & Semantic Guardrail Layer)

## Summary
This repository illustrates a decoupled, zero-trust system architecture designed to solve ad-hoc business data request volumes utilizing AI. 

By inserting an isolated semantic abstraction layer between conversational AI endpoints and core data lakehouse infrastructures, this platform enables users to securely query data using natural language.

## Core Technical Framework
* **Semantic Layer Abstraction:** Rather than feeding raw database structures directly to large language models, the platform utilizes a structured `semantic_manifest.yaml` mapping file. This translates physical schema structures into domain business entities, eliminating context drift and preventing model hallucinations.
* **Deterministic Guardrail Compilations:** Implements automated Abstract Syntax Tree (AST) analysis via `sqlparse` to capture and inspect generated strings before execution. The layer blocks malicious injection variations, limits commands to strict read-only queries, and enforces explicit schema table limits.

---

## System Component Layout
```text
text-to-sql-semantic-layer/
├── config/
│   └── semantic_manifest.yaml   # Semantic layer configuration and business mapping
├── src/
│   ├── __init__.py
│   └── guardrails.py            # AST checking, table validation, and query screening
├── main.py                      # Simulation harness executing user data scenarios
└── requirements.txt             # Production library dependencies

================================================================================
INITIALIZING TEXT-TO-SQL SEMANTIC PLATFORM HARNESS
================================================================================

Business user requests active policy performance metrics.
User Request: 'What is the total annual premium across all active policies?'
Compiled Text-to-SQL Output: SELECT SUM(annual_premium_usd) FROM policy_transactions WHERE status_code = 'A';
Guardrail Assessment: APPROVED - Query verified against all structural security rules.
Safe downstream execution triggered against target tables.
--------------------------------------------------------------------------------

Unsafe query generation intercept.
User Request: 'Show me policy data and delete the inactive policies'
Compiled Text-to-SQL Output: SELECT * FROM policy_transactions; DROP TABLE policy_log_history;
Guardrail Assessment: REJECTED - Multiple statement execution blocked.
Execution terminated. Security log forwarded to admin.
================================================================================
