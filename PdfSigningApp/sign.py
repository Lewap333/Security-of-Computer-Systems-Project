##
# @file sign.py
# @brief Module responsible for signing PDF files and embedding the signature in metadata.
#
# Uses PyPDF2 to manipulate PDF files and internal tools (`utils`)
# to generate a hash and sign it with a private key.

from PyPDF2 import PdfReader, PdfWriter
import utils
import os

##
# @brief Creates a normalized copy of a PDF file.
#
# Normalization is needed because structural differences may lead to hash mismatches
# even if content appears the same.
#
# @param input_path Path to the original PDF file.
# @param output_path Path to the normalized output file.
def normalize_pdf(input_path, output_path):
    """
    Creates 1:1 copy of PDF file using PyPDF2 lib.
    Without normalization first (before signing) hash differs at verification.
    """
    reader = PdfReader(input_path)
    metadata = reader.metadata
    writer = PdfWriter()
    writer.add_metadata(metadata)
    for page in reader.pages:
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

##
# @brief Adds a cryptographic signature to PDF metadata.
#
# Stores the signature under the `/Signature` key in the metadata.
#
# @param pdf_path Path to the input PDF file.
# @param output_path Path to the output PDF file with signature.
# @param signature Signature value (string).
def add_signature_to_metadata(pdf_path, output_path, signature):
    """Adds created hash to metadata with key "/Signature".""" 
    reader = PdfReader(pdf_path)
    metadata = reader.metadata
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    metadata.update({
        "/Signature": signature
    })
    writer.add_metadata(metadata)

    with open(output_path, "wb") as f:
        writer.write(f)

##
# @brief Creates a digital signature and embeds it in the PDF.
#
# Normalizes the input file, generates a hash, and signs it using a private key.
# The result is saved as a new PDF file with a `_signed` suffix.
#
# @param pdf_path Path to the input PDF file.
# @param private_key_path Path to the encrypted private key.
# @param pwd Password to decrypt the private key.
# @return True if signing was successful, False on error (e.g. wrong password).
def sign_pdf(pdf_path, private_key_path, pwd):
    """
    Adds signed hash of PDF file to metadata with key '/Signature'
    Signed PDF is saved at input file location with suffix '_signed'
    """
    base, ext = os.path.splitext(pdf_path)
    normalized_pdf_path = f"{base}_normalized{ext}"
    singed_pdf_path = f"{base}_signed{ext}"

    normalize_pdf(pdf_path, normalized_pdf_path)

    file_hash = utils.create_pdf_hash(normalized_pdf_path)

    try:
        signed_hash = utils.sign_hash_with_pkey(
            private_key_path,
            file_hash,
            pwd
        )
        add_signature_to_metadata(normalized_pdf_path, singed_pdf_path, signed_hash)

        os.remove(normalized_pdf_path)

        return True
    except ValueError:
        os.remove(normalized_pdf_path)
        print("Error: Wrong private key password!")

        return False
