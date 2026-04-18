from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open("fernet.key", "wb") as key_file:
    key_file.write(key)

print("🔑 Chiave generata e salvata in fernet.key")
