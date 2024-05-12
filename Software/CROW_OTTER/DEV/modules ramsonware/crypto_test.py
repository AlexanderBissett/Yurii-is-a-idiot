from cryptography.fernet import Fernet

key = Fernet.generate_key()

print(key)

with open(fr'C:\Users\udgo1\OneDrive\Escritorio\key.txt', 'wb') as f:
    f.write(key)