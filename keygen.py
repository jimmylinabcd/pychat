from cryptography.fernet import Fernet

print("Generating keys...")
key = []
for i in range(100):
    key.append(Fernet.generate_key().decode() + "\n")

f = open("keys.txt", "w")
f.write("".join(key))

f.close()
input("Done")
