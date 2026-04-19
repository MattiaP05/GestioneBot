from cryptography.fernet import Fernet

# Carica la chiave
with open("fernet.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

telegram_token = "" #Inserire le proprie API Telegram tra gli apici
openai_key = "" #inserire le proprie API di OpenIA tra gli apici

# Cifra
encrypted_telegram = fernet.encrypt(telegram_token.encode())
encrypted_openai = fernet.encrypt(openai_key.encode())

# Salva nei file
with open("telegram_token.txt", "wb") as f:
    f.write(encrypted_telegram)

with open("openai_key.txt", "wb") as f:
    f.write(encrypted_openai)

print("🔐 Token cifrati e salvati")
