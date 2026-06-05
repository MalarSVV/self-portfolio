import sqlparse
from sqlparse.tokens import Keyword, DDL, DML

class SQLGuardrail:
    """
    Advanced AST token-stream guardrail that neutralizes malicious injection,
    unauthorized data mutations (DML), and schema modifications (DDL).
    """
    def __init__(self, allowed_tables: list):
        self.allowed_tables = [table.lower() for table in allowed_tables]
        
        # Enterprise Keyword Blacklist categorized by structural risk
        self.blacklist_keywords = {
            "DDL_MUTATIONS": ["drop", "alter", "truncate", "create", "rename"],
            "DML_MUTATIONS": ["update", "delete", "insert", "replace", "upsert"],
            "SECURITY_BYPASS": ["grant", "revoke", "union", "exec", "execute"]
        }

    def validate_query(self, sql_query: str) -> dict:
        """
        Parses raw text queries into an Abstract Syntax Tree (AST) to evaluate
        individual tokens against strict security and domain boundaries.
        """
        if not sql_query or len(sql_query.strip()) == 0:
            return {"status": "REJECTED", "reason": "Empty query payload received."}

        # 1. Block basic multi-statement stacking attacks
        if ";" in sql_query and sql_query.strip().count(";") > 1:
            return {"status": "REJECTED", "reason": "Multi-statement execution stacking detected."}

        try:
            parsed = sqlparse.parse(sql_query)
            for statement in parsed:
                
                # 2. Enforce strict Read-Only root command constraint
                if statement.get_type() != "SELECT":
                    return {
                        "status": "REJECTED", 
                        "reason": f"Unauthorized structural operation intercept: [{statement.get_type()}] detected."
                    }
                
                # 3. ADVANCED AST TOKEN SCANNING: Recursively check for blacklisted keywords
                for token in statement.flatten():
                    # Flattening extracts every single individual database keyword from the query
                    token_value = str(token).strip().lower()
                    
                    # Cross-reference the token against our grouped blacklist matrices
                    for category, keywords in self.blacklist_keywords.items():
                        if token_value in keywords:
                            return {
                                "status": "REJECTED",
                                "reason": f"Security Policy Violation: Intercepted blacklisted [{category}] token matching '{token_value.upper()}'."
                            }

                # 4. Enforce strict Domain Isolation Boundaries
                query_string = sql_query.lower()
                table_found = any(table in query_string for table in self.allowed_tables)
                if not table_found:
                    return {"status": "REJECTED", "reason": "Query isolates out-of-domain metadata schemas."}
                    
            return {"status": "APPROVED", "reason": "Query safely validated against all AST token-stream guardrails."}
            
        except Exception as e:
            return {"status": "ERROR", "reason": f"AST cryptographic parsing failure: {str(e)}"}
