from PyPDF2 import PdfReader, PdfWriter
import utils
import os


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


def add_signature_to_metadata(pdf_path, output_path, signature):
    """Adds created hash to metadata with key "/Signature" and preserves existing one."""
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


def sign_pdf(pdf_path, private_key_path, pwd):
    """
    Adds signed hash of PDF file to metadata with key '/Signature'
    Singed PDF is saved at input file location with suffix '_signed'
    """
    base, ext = os.path.splitext(pdf_path)
    normalized_pdf_path = f"{base}_normalized{ext}"
    singed_pdf_path = f"{base}_signed{ext}"

    normalize_pdf(pdf_path, normalized_pdf_path)

    file_hash = utils.create_pdf_hash(normalized_pdf_path)
    # print(f"Input file hash = {file_hash.hexdigest()}")

    try:
        signed_hash = utils.sign_hash_with_pkey(
            private_key_path,
            file_hash,
            pwd
        )
        # print(f"Signed hash = {signed_hash}")
        add_signature_to_metadata(normalized_pdf_path, singed_pdf_path, signed_hash)

        os.remove(normalized_pdf_path)

        return True
    except ValueError:
        os.remove(normalized_pdf_path)
        print("Error: Wrong private key password!")

        return False
