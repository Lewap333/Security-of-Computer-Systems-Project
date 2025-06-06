##
# @file utils.py
# @brief Contains cryptographic utility functions for PDF hashing, key generation, and digital signatures.
#
# This module provides support for creating SHA-256 hashes of PDF files,
# generating RSA key pairs, and signing hashes with private keys.

import time
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import os

##
# @brief Creates a SHA-256 hash of the given PDF file.
# @param pdf_path Path to the input PDF file.
# @return SHA-256 hash object of the file content.
def create_pdf_hash(pdf_path):
    """Create SHA-256 hash of a PDF file."""
    with open(pdf_path, "rb") as f:
        data = f.read()
    h = SHA256.new(data)
    return h

##
# @brief Generates a 4096-bit RSA key pair and saves it to the specified directory.
#
# The private key is encrypted using AES-256 with the provided password.
#
# @param dir_path Directory path where the keys should be saved.
# @param pwd Password used to encrypt the private key.
def generate_key_pair(dir_path, pwd):
    start = time.time()

    key = RSA.generate(4096)
    print(f"RSA key generation time: {time.time() - start:.2f} seconds")

    start = time.time()
    private_key_encrypted = key.export_key(
        passphrase=pwd,
        pkcs=8,
        protection="scryptAndAES256-CBC"
    )
    print(f"Private key encryption time (AES): {time.time() - start:.2f} seconds")

    public_key = key.publickey().export_key()

    private_key_path = os.path.join(dir_path, "private_key.pem")
    public_key_path = os.path.join(dir_path, "public_key.pem")

    with open(public_key_path, "wb") as f:
        f.write(public_key)

    with open(private_key_path, "wb") as f:
        f.write(private_key_encrypted)

##
# @brief Signs a hash using a private RSA key loaded from a PEM file.
#
# @param pkey_path Path to the PEM-formatted private key file.
# @param file_hash Hash object to be signed (e.g., SHA-256 hash).
# @param pwd Password to decrypt the private key.
# @return Hexadecimal string of the generated signature.
def sign_hash_with_pkey(pkey_path, file_hash, pwd):
    with open(pkey_path, "rb") as f:
        private_key_pem = f.read()

    private_key = RSA.import_key(private_key_pem, passphrase=pwd)
    signature = pkcs1_15.new(private_key).sign(file_hash)
    return signature.hex()
