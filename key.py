from cryptography.fernet import Fernet

# Generate the key
key = Fernet.generate_key()

# Save the key to a file called 'key.key'
with open('key.key', 'wb') as key_file:
    key_file.write(key)

print("Encryption key has been saved to 'key.key'.")