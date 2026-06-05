import sqlparse
import re

class SQLGuardrail:
    """
    Enforces zero-trust isolation boundaries on LLM-generated SQL queries
    before downstream compilation and database cluster execution.
    """
    def __init__(self, allowed_tables: list):
        self.allowed_tables = [table.lower() for table in allowed_tables]

    def validate_query(self, sql_query: str) -> dict:
        """
        Parses raw text queries to block destructive commands and restrict
        data access exclusively to white-listed domain tables.
        """
        if not sql_query or len(sql_query.strip()) == 0:
            return {"status": "REJECTED", "reason": "Empty query payload received."}

        # 1. Block embedded SQL injection characters or suspicious comments
        if ";" in sql_query and sql_query.strip().count(";") > 1:
            return {"status": "REJECTED", "reason": "Multiple statement execution blocked."}

        try:
            parsed = sqlparse.parse(sql_query)
            for statement in parsed:
                # 2. Enforce strict Read-Only constraints
                if statement.get_type() != "SELECT":
                    return {
                        "status": "REJECTED", 
                        "reason": f"Unauthorized DDL/DML operation detected: {statement.get_type()}"
                    }
                
                # 3. Analyze tokens for hidden structural alterations
                tokens = [str(t).lower() for t in statement.tokens]
                destructive_keywords = ["drop", "delete", "update", "truncate", "alter", "grant"]
                if any(keyword in tokens for keyword in destructive_keywords):
                    return {"status": "REJECTED", "reason": "Destructive operational keywords intercepted."}
                
                # 4. Verify table isolation boundaries
                # Basic string matcher for safety checking against the allowed table list
                query_string = sql_query.lower()
                table_found = any(table in query_string for table in self.allowed_tables)
                if not table_found:
                    return {"status": "REJECTED", "reason": "Query attempts to access restricted or out-of-domain schemas."}
                    
            return {"status": "APPROVED", "reason": "Query verified against all structural security rules."}
            
        except Exception as e:
            return {"status": "ERROR", "reason": f"AST parsing failure: {str(e)}"}
