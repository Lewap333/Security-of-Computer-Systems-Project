import sign as s
import verify as v
import utils as u

# tylko testowo nie ma jeszcze integracji z gui

# generowanie pary kluczy w pytonie (trwa troche dluzej niz to z openssl ale < 20sec)
# u.generate_key_pair("C:\\Git", "1234")

s.sign_pdf("C:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\sample-1.pdf", "C:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\private_key.pem", "1234")

v.verify_pdf("C:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\sample-1_signed.pdf", "C:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\public_key.pem")