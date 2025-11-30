import json

def create_schemas():
    # V1: Simple User
    v1_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]
    
    # V2: Breaking Changes!
    # - 'name' split into 'first_name' and 'last_name' (Breaking)
    # - 'email' removed (Breaking)
    # - 'age' added (Non-breaking if optional)
    v2_data = [
        {"id": 3, "first_name": "Charlie", "last_name": "Brown", "age": 30},
        {"id": 4, "first_name": "David", "last_name": "Smith", "age": 40}
    ]
    
    with open('data_v1.json', 'w') as f:
        json.dump(v1_data, f, indent=2)
        
    with open('data_v2.json', 'w') as f:
        json.dump(v2_data, f, indent=2)
        
    print("✅ Created data_v1.json and data_v2.json")

if __name__ == "__main__":
    create_schemas()
