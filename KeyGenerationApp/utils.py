##
# @file utils.py
# @brief Module responsible for generating RSA key pairs and saving them to files.
#
# Generates a 4096-bit RSA key pair, encrypts the private key with a passphrase using AES-256,
# and saves both keys in PEM format to the specified directories.

import time
from Cryptodome.PublicKey import RSA
import os

##
# @brief Generates and saves a 4096-bit RSA key pair.
#
# The private key is encrypted using AES-256 (via scrypt + CBC) and saved to the provided path.
# The public key is saved in plain text to the specified output directory.
#
# @param dir_path Path to directory where the public key will be saved.
# @param priv_path Path to directory where the private key will be saved.
# @param pwd Passphrase to encrypt the private key with AES-256.
#
# @return None
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
