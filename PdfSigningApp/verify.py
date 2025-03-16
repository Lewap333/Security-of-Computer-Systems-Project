from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter
import utils
import os


def verify_pdf(pdf_path, public_key_path):
    """
    Extracts the signature from the metadata at the key /Signature.
    Creates a temporary copy of the input PDF file and generates a hash from its contents.
    Verifies the generated hash against the extracted signature using the provided public key.
    """
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

    # Clean version of the file as path_temp.pdf (without signature in metadata)
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



