import json
import os
from datetime import datetime

class EC2Instance:
    def __init__(self, instance_id, instance_type, region):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.region = region
        self.state = "unknown"

    def to_dict(self):
        return {
            "type": "EC2",
            "id": self.instance_id,
            "instance_type": self.instance_type,
            "region": self.region,
            "state": self.state
        }

    def describe(self):
        return f"EC2: {self.instance_id} ({self.instance_type}) in {self.region} - State: {self.state}"

class S3Bucket:
    def __init__(self, bucket_name, region):
        self.bucket_name = bucket_name
        self.region = region
        self.size_gb = 0
        self.files = 0

    def to_dict(self):
        return {
            "type": "S3",
            "name": self.bucket_name,
            "region": self.region,
            "size_gb": self.size_gb,
            "files": self.files
        }

    def describe(self):
        return f"S3: {self.bucket_name} ({self.size_gb} GB, {self.files} files) in {self.region}"

def save_inventory(resources, filename="inventory.json"):
    data_to_save = {
        "timestamp": datetime.now().isoformat(),
        "resources": [r.to_dict() for r in resources]
    }
    with open(filename, 'w') as f:
        json.dump(data_to_save, f, indent=2)
    print(f"✅ Saved {len(resources)} resources to {filename}")

def load_inventory(filename="inventory.json"):
    if not os.path.exists(filename):
        print(f"❌ File {filename} not found")
        return []
    with open(filename, 'r') as f:
        data = json.load(f)
    print(f"📅 Data saved at: {data['timestamp']}")
    print(f"✅ Loaded {len(data['resources'])} resources")
    return data['resources']

def update_resource(filename, resource_id, updates):
    with open(filename, 'r') as f:
        data = json.load(f)

    found = False
    for resource in data['resources']:
        if resource.get('id') == resource_id or resource.get('name') == resource_id:
            resource.update(updates)
            found = True
            print(f"✅ Updated {resource_id} with {updates}")
            break

    if not found:
        print(f"❌ Resource {resource_id} not found")
        return

    data['timestamp'] = datetime.now().isoformat()
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# ===== MAIN PROGRAM =====

print("=" * 60)
print("  AWS Resource Inventory Manager")
print("=" * 60)

# Create resources
ec2_1 = EC2Instance("i-04bf3604535fa43ef", "t3.micro", "ap-south-1")
ec2_1.state = "running"

ec2_2 = EC2Instance("i-12345678abcd", "t3.small", "us-east-1")
ec2_2.state = "stopped"

s3_1 = S3Bucket("akshay-devops-2026", "ap-south-1")
s3_1.size_gb = 8
s3_1.files = 2

s3_2 = S3Bucket("logs-backup", "us-east-1")
s3_2.size_gb = 10
s3_2.files = 1

all_resources = [ec2_1, ec2_2, s3_1, s3_2]

# Save
save_inventory(all_resources)

# Update
print("\n=== Testing Update ===")
update_resource("inventory.json", "i-04bf3604535fa43ef", {"state": "stopped"})

# Load and verify
print("\n=== Verifying Update ===")
loaded = load_inventory()
for r in loaded:
    if r.get('id') == "i-04bf3604535fa43ef":
        print(f"New state: {r['state']}")
def delete_resource(filename, resource_id):
    with open(filename, 'r') as f:
        data = json.load(f)

    original_count = len(data['resources'])
    data['resources'] = [
        r for r in data['resources']
        if r.get('id') != resource_id and r.get('name') != resource_id
    ]

    if len(data['resources']) == original_count:
        print(f"❌ Resource {resource_id} not found")
        return

    data['timestamp'] = datetime.now().isoformat()
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"🗑️  Deleted {resource_id} from inventory")

# Test delete
print("\n=== Testing Delete ===")
delete_resource("inventory.json", "i-12345678abcd")
loaded = load_inventory()
print(f"Resources remaining: {len(loaded)}")
