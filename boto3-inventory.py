import boto3
import json
import os
from datetime import datetime

# ===== CLASSES =====

class EC2Instance:
    def __init__(self, instance_id, instance_type, region, state):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.region = region
        self.state = state

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
    def __init__(self, bucket_name, creation_date):
        self.bucket_name = bucket_name
        self.creation_date = creation_date

    def to_dict(self):
        return {
            "type": "S3",
            "name": self.bucket_name,
            "created": self.creation_date
        }

    def describe(self):
        return f"S3: {self.bucket_name} (created: {self.creation_date})"

# ===== FETCH FROM REAL AWS =====

def fetch_ec2_instances(region="ap-south-1"):
    """Pull real EC2 instances from AWS"""
    print(f"\n🔍 Fetching EC2 instances from AWS ({region})...")
    
    ec2 = boto3.client('ec2', region_name=region)
    instances = []
    
    try:
        response = ec2.describe_instances()
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                obj = EC2Instance(
                    instance_id=instance['InstanceId'],
                    instance_type=instance['InstanceType'],
                    region=region,
                    state=instance['State']['Name']
                )
                instances.append(obj)
                print(f"  Found: {obj.describe()}")
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return instances

def fetch_s3_buckets():
    """Pull real S3 buckets from AWS"""
    print(f"\n🔍 Fetching S3 buckets from AWS...")
    
    s3 = boto3.client('s3')
    buckets = []
    
    try:
        response = s3.list_buckets()
        
        for bucket in response['Buckets']:
            obj = S3Bucket(
                bucket_name=bucket['Name'],
                creation_date=bucket['CreationDate'].strftime('%Y-%m-%d')
            )
            buckets.append(obj)
            print(f"  Found: {obj.describe()}")
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return buckets

def save_inventory(resources, filename="real-inventory.json"):
    """Save fetched resources to JSON file"""
    data = {
        "timestamp": datetime.now().isoformat(),
        "source": "AWS Live",
        "resources": [r.to_dict() for r in resources]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n💾 Saved {len(resources)} real resources to {filename}")

# ===== MAIN =====

print("=" * 60)
print("  Real AWS Inventory — Boto3")
print("=" * 60)

# Fetch real data
ec2_instances = fetch_ec2_instances(region="ap-south-1")
s3_buckets = fetch_s3_buckets()

# Combine all resources
all_resources = ec2_instances + s3_buckets

# Save to file
save_inventory(all_resources)

# Show summary
print("\n=== Summary ===")
print(f"EC2 Instances: {len(ec2_instances)}")
print(f"S3 Buckets:    {len(s3_buckets)}")
print(f"Total:         {len(all_resources)}")

print("\n✅ Real inventory complete!")
def fetch_iam_users():
    """Pull real IAM users from AWS"""
    print(f"\n🔍 Fetching IAM users from AWS...")

    iam = boto3.client('iam')
    users = []

    try:
        response = iam.list_users()

        for user in response['Users']:
            groups = iam.list_groups_for_user(UserName=user['UserName'])
            group_names = [g['GroupName'] for g in groups['Groups']]

            users.append({
                "type": "IAM",
                "username": user['UserName'],
                "created": user['CreateDate'].strftime('%Y-%m-%d'),
                "groups": group_names
            })
            print(f"  Found: {user['UserName']} → {group_names}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    return users

# Fetch IAM and show
iam_users = fetch_iam_users()
print(f"\nIAM Users: {len(iam_users)}")
for u in iam_users:
    print(f"  👤 {u['username']} → {u['groups']}")
