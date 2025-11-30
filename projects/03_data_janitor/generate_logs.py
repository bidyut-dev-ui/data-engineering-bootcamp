import json
import random
import time
from datetime import datetime, timedelta

def generate_logs(num_files=5, lines_per_file=1000):
    print(f"Generating {num_files} log files...")
    
    actions = ['login', 'logout', 'view_item', 'add_to_cart', 'checkout', 'error']
    user_agents = ['Mozilla/5.0', 'Chrome/90.0', 'Safari/14.0', 'Bot/1.0']
    
    start_time = datetime.now() - timedelta(days=1)
    
    for i in range(num_files):
        filename = f"data/raw/server_log_{i}.jsonl"
        with open(filename, 'w') as f:
            for _ in range(lines_per_file):
                # Create a log entry
                log = {
                    'timestamp': (start_time + timedelta(seconds=random.randint(0, 86400))).isoformat(),
                    'user_id': random.randint(1000, 9999),
                    'action': random.choice(actions),
                    'metadata': {
                        'ip': f"192.168.1.{random.randint(1, 255)}",
                        'user_agent': random.choice(user_agents)
                    }
                }
                
                # Introduce messiness
                if random.random() < 0.05:
                    del log['timestamp'] # Missing timestamp
                if random.random() < 0.05:
                    log['action'] = log['action'].upper() # Inconsistent casing
                
                f.write(json.dumps(log) + '\n')
                
        print(f"Created {filename}")

if __name__ == "__main__":
    generate_logs()
