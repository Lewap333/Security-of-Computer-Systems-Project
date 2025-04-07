import time

from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import os


def create_pdf_hash(pdf_path):
    """Create SHA-256 hash of a PDF file."""
    with open(pdf_path, "rb") as f:
        data = f.read()

    h = SHA256.new(data)

    return h


def generate_key_pair(dir_path, pwd):

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

    private_key_path = os.path.join(dir_path, "private_key.pem")
    public_key_path = os.path.join(dir_path, "public_key.pem")

    with open(public_key_path, "wb") as f:
        f.write(public_key)

    with open(private_key_path, "wb") as f:
        f.write(private_key_encrypted)


def sign_hash_with_pkey(pkey_path, file_hash, pwd):

    with open(pkey_path, "rb") as f:
        private_key_pem = f.read()

    private_key = RSA.import_key(private_key_pem, passphrase=pwd)

    signature = pkcs1_15.new(private_key).sign(file_hash)

    return signature.hex()
