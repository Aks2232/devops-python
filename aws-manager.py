import boto3
import sys

ec2 = boto3.client('ec2', region_name='ap-south-1')
s3 = boto3.client('s3')
iam = boto3.client('iam')

def get_ec2_info():
    """Get all EC2 instances and their details"""
    print("\n=== EC2 Instances ===")
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                ip = instance.get('PublicIpAddress', 'No IP')
                instance_type = instance['InstanceType']
                print(f"  {instance_id} | {state} | {instance_type} | {ip}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def get_s3_info():
    """Get all S3 buckets"""
    print("\n=== S3 Buckets ===")
    try:
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            name = bucket['Name']
            created = bucket['CreationDate'].strftime('%Y-%m-%d')
            print(f"  📦 {name} (created: {created})")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def get_iam_info():
    """Get all IAM users and their groups"""
    print("\n=== IAM Users ===")
    try:
        response = iam.list_users()
        for user in response['Users']:
            username = user['UserName']
            groups = iam.list_groups_for_user(UserName=username)
            group_names = [g['GroupName'] for g in groups['Groups']]
            group_str = ", ".join(group_names) if group_names else "No groups"
            print(f"  👤 {username} → [{group_str}]")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def get_security_groups():
    """Check security groups for open access"""
    print("\n=== Security Group Audit ===")
    try:
        response = ec2.describe_security_groups()
        for sg in response['SecurityGroups']:
            name = sg['GroupName']
            sg_id = sg['GroupId']
            print(f"\n  🔒 {name} ({sg_id})")
            for rule in sg['IpPermissions']:
                port = rule.get('FromPort', 'All')
                for ip_range in rule.get('IpRanges', []):
                    cidr = ip_range['CidrIp']
                    if cidr == '0.0.0.0/0':
                        print(f"     ⚠️  Port {port} open to EVERYONE")
                    else:
                        print(f"     ✅ Port {port} open to {cidr}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

# Main menu
print("=" * 40)
print("  AWS Resource Manager (Python)")
print(f"  Run at: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 40)

get_ec2_info()
get_s3_info()
get_iam_info()
get_security_groups()

print("\n✅ Report complete!")