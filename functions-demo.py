# Functions and error handling

def check_status(service, status):
    """Check if a service is healthy"""
    if status == "running":
        return f"✅ {service} is healthy"
    elif status == "stopped":
        return f"❌ {service} is down"
    else:
        return f"⚠️ {service} is in state: {status}"

# Using the function
services = [
    {"name": "EC2 Instance", "status": "running"},
    {"name": "Database", "status": "stopped"},
    {"name": "Nginx", "status": "running"},
    {"name": "Redis Cache", "status": "unknown"},
]

print("=== Service Health Check ===\n")
for service in services:
    result = check_status(service["name"], service["status"])
    print(result)

# Error handling with try/except
print("\n=== Error Handling Demo ===\n")

try:
    number = int("abc")
except ValueError:
    print("Caught an error: 'abc' is not a number")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Caught an error: can't divide by zero")

print("\nScript completed without crashing!")