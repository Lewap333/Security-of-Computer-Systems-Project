import time
from Cryptodome.PublicKey import RSA
import os


def generate_key_pair(dir_path, priv_path, pwd):

    start = time.time()

    key = RSA.generate(4096)

    print(f"Czas generowania RSA: {time.time() - start:.2f} sekundy")

    start = time.time()
    private_key_encrypted = key.export_key(
        passphrase=pwd,
        pkcs=8,
        protection="scryptAndAES256-CBC"
    )

    print(f"Czas AES: {time.time() - start:.2f} sekundy")

    public_key = key.publickey().export_key()

    private_key_path = os.path.join(priv_path, "private_key.pem")
    public_key_path = os.path.join(dir_path, "public_key.pem")

    with open(public_key_path, "wb") as f:
        f.write(public_key)

    with open(private_key_path, "wb") as f:
        f.write(private_key_encrypted)

