import hmac
import hashlib
import sys

message = (sys.argv[1]).encode()

secret_key = b"your_secret_key_here"

#message = "This is a secret message"

# # Encode message if it's a string
# if isinstance(message, str):
#     message = message.encode()

# Choose a digest algorithm (e.g. SHA-256)
digestmod = hashlib.sha256

# Create hmac object
h = hmac.new(secret_key, message, digestmod)

# Get the HMAC digest in hexadecimal format
hmac_value = h.hexdigest()

print(hmac_value)