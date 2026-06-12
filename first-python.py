# My first Python script

name = "Akshay"
role = "IT Support Specialist"
target = "DevOps Engineer"

print(f"Name: {name}")
print(f"Current Role: {role}")
print(f"Target Role: {target}")

skills_learned = ["Linux", "AWS EC2", "AWS S3", "Bash", "Git"]
skills_to_learn = ["Python", "Docker", "Terraform", "Kubernetes"]

print(f"\nSkills I know: {len(skills_learned)}")
for skill in skills_learned:
    print(f"  ✅ {skill}")

print(f"\nSkills to learn: {len(skills_to_learn)}")
for skill in skills_to_learn:
    print(f"  📘 {skill}")

my_aws = {
    "instance_id": "i-04bf3604535fa43ef",
    "region": "ap-south-1",
    "buckets": 4,
    "status": "learning"
}

print(f"\nMy AWS Setup:")
for key, value in my_aws.items():
    print(f"  {key}: {value}")