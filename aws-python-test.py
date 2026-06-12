import boto3

ec2 = boto3.client('ec2', region_name='ap-south-1')

response = ec2.describe_instances(InstanceIds=['i-04bf3604535fa43ef'])
state = response['Reservations'][0]['Instances'][0]['State']['Name']
ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'No IP')

print(f"EC2 Status: {state}")
print(f"Public IP: {ip}")

s3 = boto3.client('s3')
buckets = s3.list_buckets()

print(f"\nS3 Buckets:")
for bucket in buckets['Buckets']:
    print(f"  📦 {bucket['Name']}")