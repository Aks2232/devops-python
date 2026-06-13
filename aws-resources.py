# AWS Resource Classes - Week 12

class EC2Instance:
    """Represents an EC2 instance"""
    
    def __init__(self, instance_id, instance_type, region):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.region = region
        self.state = "unknown"
    
    def describe(self):
        """Show instance details"""
        return f"EC2: {self.instance_id} ({self.instance_type}) in {self.region} - State: {self.state}"
    
    def set_state(self, state):
        """Update the state"""
        self.state = state
        return f"✅ {self.instance_id} is now {state}"
    
    def get_info(self):
        """Return all info as dictionary"""
        return {
            "id": self.instance_id,
            "type": self.instance_type,
            "region": self.region,
            "state": self.state
        }

class S3Bucket:
    """Represents an S3 bucket"""
    
    def __init__(self, bucket_name, region):
        self.bucket_name = bucket_name
        self.region = region
        self.size_gb = 0
        self.files = 0
    
    def describe(self):
        """Show bucket details"""
        return f"S3: {self.bucket_name} ({self.size_gb} GB, {self.files} files) in {self.region}"
    
    def add_file(self, size_gb):
        """Add a file to bucket"""
        self.size_gb += size_gb
        self.files += 1
        return f"📦 Added file ({size_gb}GB) to {self.bucket_name}"
    
    def get_info(self):
        """Return all info as dictionary"""
        return {
            "name": self.bucket_name,
            "region": self.region,
            "size_gb": self.size_gb,
            "files": self.files
        }

# ===== MAIN PROGRAM =====

print("=" * 50)
print("  AWS Resource Manager - OOP Style")
print("=" * 50)

# Create EC2 instances
print("\n=== EC2 Instances ===")
ec2_1 = EC2Instance("i-04bf3604535fa43ef", "t3.micro", "ap-south-1")
ec2_2 = EC2Instance("i-12345678abcd", "t3.small", "us-east-1")

ec2_1.set_state("running")
ec2_2.set_state("stopped")

print(ec2_1.describe())
print(ec2_2.describe())

# Create S3 buckets
print("\n=== S3 Buckets ===")
s3_1 = S3Bucket("akshay-devops-2026", "ap-south-1")
s3_2 = S3Bucket("logs-backup", "us-east-1")

s3_1.add_file(5)
s3_1.add_file(3)
s3_2.add_file(10)

print(s3_1.describe())
print(s3_2.describe())

# Store all resources in a list
print("\n=== All Resources Summary ===")
all_resources = [ec2_1, ec2_2, s3_1, s3_2]

for resource in all_resources:
    print(f"  • {resource.describe()}")

# Get detailed info
print("\n=== Detailed Information ===")
print("EC2-1 info:", ec2_1.get_info())
print("S3-1 info:", s3_1.get_info())

print("\n✅ Class-based resource management complete!")