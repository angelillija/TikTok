import hashlib

# Add your urlencoded request body
data = ""

print(hashlib.md5(data.encode()).hexdigest().upper())
