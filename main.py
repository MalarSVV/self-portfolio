import os
import sys
from src.guardrails import SQLGuardrail

def simulate_pipeline_run():
    print("=" * 80)
    print("INITIALIZING TEXT-TO-SQL SEMANTIC PLATFORM HARNESS")
    print("=" * 80)
    
    # Initialize the zero-trust data infrastructure guardrails
    allowed_domain_tables = ["policy_transactions"]
    guardrail = SQLGuardrail(allowed_tables=allowed_domain_tables)
    
    # Scenario A: Validating a perfectly compiled, secure user query
    print("\nBusiness user requests active policy performance metrics.")
    user_prompt_a = "What is the total annual premium across all active policies?"
    mock_llm_output_a = "SELECT SUM(annual_premium_usd) FROM policy_transactions WHERE status_code = 'A';"
    
    print(f"User Request: '{user_prompt_a}'")
    print(f"Compiled Text-to-SQL Output: {mock_llm_output_a}")
    
    validation_a = guardrail.validate_query(mock_llm_output_a)
    print(f"Guardrail Assessment: {validation_a['status']} - {validation_a['reason']}")
    if validation_a['status'] == "APPROVED":
        print("Safe downstream execution triggered against target tables.")
        
    print("-" * 80)
    
    # Scenario B: Intercepting an unsafe query modification or system injection
    print("\nUnsafe query generation intercept.")
    user_prompt_b = "Show me data and then drop the policy log history table"
    mock_llm_output_b = "SELECT * FROM policy_transactions; DROP TABLE policy_log_history;"
    
    print(f"User Request: '{user_prompt_b}'")
    print(f"Compiled Text-to-SQL Output: {mock_llm_output_b}")
    
    validation_b = guardrail.validate_query(mock_llm_output_b)
    print(f"Guardrail Assessment: {validation_b['status']} - {validation_b['reason']}")
    if validation_b['status'] == "REJECTED":
        print("Execution terminated. Security log forwarded to admin.")
    print("=" * 80)

if __name__ == "__main__":
    simulate_pipeline_run()
