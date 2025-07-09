import base64
import os

# Generate a secure random 256-bit (32-byte) key
secret_key = os.urandom(32)
# Encode it in Base64 for easy use in properties files
encoded_key = base64.urlsafe_b64encode(secret_key).decode('utf-8')

print("Your generated JWT secret key (Base64 encoded):")
print(encoded_key)
print("\nCopy this string and paste it into your application.properties for 'jwt.secret'.")