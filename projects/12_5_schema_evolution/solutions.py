#!/usr/bin/env python3
"""
Solutions for Schema Evolution Practice Exercises
"""

import json
from typing import Dict, List, Any
import re

def solution_1_validation(data: Dict, schema: Dict) -> Dict[str, Any]:
    errors = []
    for field, rules in schema.items():
        # 1. Required check
        if rules.get("required") and field not in data:
            errors.append(f"Missing required field: {field}")
            continue
        
        if field in data:
            val = data[field]
            # 2. Type check
            expected_type = rules.get("type")
            if expected_type == "integer" and not isinstance(val, int):
                errors.append(f"Field {field} must be integer, got {type(val).__name__}")
            elif expected_type == "string" and not isinstance(val, str):
                errors.append(f"Field {field} must be string, got {type(val).__name__}")
            elif expected_type == "object" and not isinstance(val, dict):
                errors.append(f"Field {field} must be object, got {type(val).__name__}")
            
            # 3. Constraint checks
            if expected_type == "string" and "pattern" in rules:
                if not re.match(rules["pattern"], val):
                    errors.append(f"Field {field} does not match pattern {rules['pattern']}")
            
            if expected_type == "integer":
                if "min" in rules and val < rules["min"]:
                    errors.append(f"Field {field} below minimum {rules['min']}")
                if "max" in rules and val > rules["max"]:
                    errors.append(f"Field {field} above maximum {rules['max']}")
                    
    return {"valid": len(errors) == 0, "errors": errors, "data": data}

def solution_3_adapter(data: Dict, target_schema: Dict) -> Dict:
    # Field mapping: new -> target
    mapping = {
        "user_id": "id",
        "email_address": "email",
        "years_old": "age",
        "registration_timestamp": "signup_date"
    }
    
    adapted = {}
    # 1. Direct mappings
    for old_key, new_key in mapping.items():
        adapted[new_key] = data.get(old_key)
        
    # 2. Derived fields (Full Name)
    if "first_name" in data and "last_name" in data:
        adapted["full_name"] = f"{data['first_name']} {data['last_name']}"
    
    # 3. Defaults
    if adapted.get("signup_date") is None:
        adapted["signup_date"] = "1970-01-01T00:00:00Z"
        
    return adapted

if __name__ == "__main__":
    print("Testing Validation Solution...")
    schema = {"user_id": {"type": "integer", "required": True}}
    print(solution_1_validation({"user_id": "not_int"}, schema))
    
    print("\nTesting Adapter Solution...")
    incoming = {"user_id": 1, "first_name": "Alice", "last_name": "Smith"}
    print(solution_3_adapter(incoming, {}))
