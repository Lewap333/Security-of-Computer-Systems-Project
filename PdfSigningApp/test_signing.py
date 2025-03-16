import sign as s
import verify as v

s.sign_pdf("S:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\sample-1.pdf", "S:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\private_key.pem", "1234")

v.verify_pdf("S:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\sample-1_signed.pdf", "S:\\Git\\Security-of-Computer-Systems-Project\\PdfSigningApp\\public_key.pem")