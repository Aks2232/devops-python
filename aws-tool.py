import argparse
import boto3
import json
from datetime import datetime

# ===== STEP 1: Define what arguments your tool accepts =====

parser = argparse.ArgumentParser(
    description="AWS Resource Manager - fetch and manage your AWS resources"
)

parser.add_argument(
    "--list-ec2",
    action="store_true",
    help="List all EC2 instances"
)

parser.add_argument(
    "--list-s3",
    action="store_true",
    help="List all S3 buckets"
)

parser.add_argument(
    "--list-iam",
    action="store_true",
    help="List all IAM users"
)

parser.add_argument(
    "--region",
    default="ap-south-1",
    help="AWS region to use (default: ap-south-1)"
)

parser.add_argument(
    "--save",
    action="store_true",
    help="Save results to a JSON file"
)

# ===== STEP 2: Read what the user typed =====

args = parser.parse_args()

# ===== STEP 3: Functions that do the actual work =====

def list_ec2(region):
    print(f"\n=== EC2 Instances ({region}) ===")
    ec2 = boto3.client('ec2', region_name=region)
    
    try:
        response = ec2.describe_instances()
        instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']
                ip = instance.get('PublicIpAddress', 'No IP')
                
                print(f"  ID:     {instance_id}")
                print(f"  Type:   {instance_type}")
                print(f"  State:  {state}")
                print(f"  IP:     {ip}")
                print()
                
                instances.append({
                    "type": "EC2",
                    "id": instance_id,
                    "instance_type": instance_type,
                    "state": state,
                    "ip": ip,
                    "region": region
                })
        
        if not instances:
            print("  No EC2 instances found.")
        
        return instances
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def list_s3():
    print(f"\n=== S3 Buckets ===")
    s3 = boto3.client('s3')
    
    try:
        response = s3.list_buckets()
        buckets = []
        
        for bucket in response['Buckets']:
            name = bucket['Name']
            created = bucket['CreationDate'].strftime('%Y-%m-%d')
            
            print(f"  📦 {name}  (created: {created})")
            
            buckets.append({
                "type": "S3",
                "name": name,
                "created": created
            })
        
        if not buckets:
            print("  No S3 buckets found.")
        
        return buckets
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def list_iam():
    print(f"\n=== IAM Users ===")
    iam = boto3.client('iam')
    
    try:
        response = iam.list_users()
        users = []
        
        for user in response['Users']:
            username = user['UserName']
            created = user['CreateDate'].strftime('%Y-%m-%d')
            groups = iam.list_groups_for_user(UserName=username)
            group_names = [g['GroupName'] for g in groups['Groups']]
            
            print(f"  👤 {username}")
            print(f"     Created: {created}")
            print(f"     Groups:  {group_names}")
            print()
            
            users.append({
                "type": "IAM",
                "username": username,
                "created": created,
                "groups": group_names
            })
        
        if not users:
            print("  No IAM users found.")
        
        return users
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def save_to_file(data, filename="aws-tool-output.json"):
    output = {
        "timestamp": datetime.now().isoformat(),
        "resources": data
    }
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n💾 Saved to {filename}")

# ===== STEP 4: Run only what the user asked for =====

print("=" * 50)
print("  AWS Resource Manager")
print("=" * 50)

results = []

if args.list_ec2:
    ec2_data = list_ec2(args.region)
    results.extend(ec2_data)

if args.list_s3:
    s3_data = list_s3()
    results.extend(s3_data)

if args.list_iam:
    iam_data = list_iam()
    results.extend(iam_data)

if args.save and results:
    save_to_file(results)

# If user typed nothing, show help
if not any([args.list_ec2, args.list_s3, args.list_iam]):
    print("\n  No option selected. Use --help to see available commands.")
    parser.print_help()