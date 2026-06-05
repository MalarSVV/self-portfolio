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
│
├── config/
│   └── semantic_manifest.yaml   # Semantic layer configuration and business metadata mapping
│
├── data/
│   └── schema_seed.sql          # Target analytical data warehouse/DB layout blueprint
│
├── src/
│   ├── __init__.py              # Package initialization hook
│   ├── guardrails.py            # Advanced AST token-stream scanner & grouped keyword blacklists
│   └── llm_agent.py             # Context compiler prompt engine and deterministic mock generation
│
├── main.py                      # Multi-scenario integration harness (Happy, DDL, and DML paths)
├── requirements.txt             # Production dependency tracking matrix
└── README.md                    # Core documentation system and execution validation logs

## Verified Pipeline Execution Logs

================================================================================
INITIALIZING TEXT-TO-SQL SEMANTIC GUARDRAIL HARNESS
================================================================================

[SCENARIO A] Business User Requesting Metric Performance Aggregations...
User Request:  'What is the total annual premium across all active policies?'
Compiled SQL:  SELECT SUM(annual_premium_usd) FROM policy_transactions WHERE status_code = 'A';
Policy Action: APPROVED -> Query safely validated against all AST token-stream guardrails.
Result: Forwarding query token stream directly to downstream database compute nodes.
--------------------------------------------------------------------------------

[SCENARIO B] Adversarial Prompt Injection - Malicious DDL Intercept...
User Request:  'Show me data and then drop the policy log history table'
Compiled SQL:  SELECT * FROM policy_transactions; DROP TABLE policy_log_history;
Policy Action: REJECTED -> Multi-statement execution stacking detected.
Result: Dropping query connection pipeline immediately. Incident logged.
--------------------------------------------------------------------------------

[SCENARIO C] Unauthorized Sub-Query Mutation - Data Edit Attempt...
User Request:  'Show me active policies but update the premium rate of POL-99421 to zero'
Compiled SQL:  SELECT * FROM policy_transactions WHERE policy_id IN (UPDATE policy_transactions SET annual_premium_usd = 0.00);
Policy Action: REJECTED -> Security Policy Violation: Intercepted blacklisted [DML_MUTATIONS] token matching 'UPDATE'.
Result: Write attempt blocked. Conversational AI interface is locked to Read-Only operations.
================================================================================
