##
# @file verify.py
# @brief Provides functionality to verify a digitally signed PDF using RSA and SHA-256.
#
# This module extracts the digital signature from a PDF's metadata,
# reconstructs a clean copy without the signature, generates its hash,
# and validates the signature using a provided RSA public key.

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter
import utils
import os

##
# @brief Verifies the digital signature of a PDF file.
#
# This function reads the embedded signature from the metadata (under `/Signature` key),
# removes the signature from the metadata to obtain a clean version of the PDF,
# creates a SHA-256 hash of this clean copy, and then verifies the hash against
# the stored signature using the provided RSA public key.
#
# @param pdf_path Path to the signed PDF file.
# @param public_key_path Path to the public key file (PEM format).
# @return True if the signature is valid and the PDF was not modified; False otherwise.
def verify_pdf(pdf_path, public_key_path):
    base, ext = os.path.splitext(pdf_path)
    temp_pdf_path = f"{base}_temp{ext}"

    reader = PdfReader(pdf_path)
    metadata = reader.metadata

    try:
        stored_signature = metadata.pop("/Signature")
    except KeyError:
        print("No signature in given file")
        return False

    signature_bytes = bytes.fromhex(stored_signature)

    # Create a clean version of the PDF without the signature
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(metadata)

    with open(temp_pdf_path, "wb") as f:
        writer.write(f)

    new_hash = utils.create_pdf_hash(temp_pdf_path)
    os.remove(temp_pdf_path)

    with open(public_key_path, "rb") as f:
        public_key_data = f.read()

    try:
        public_key = RSA.import_key(public_key_data)
        pkcs1_15.new(public_key).verify(new_hash, signature_bytes)
        print("Signature is valid! File not modified! ✅")
        return True
    except ValueError:
        print("Invalid signature! File was modified! ❌")
        return False
