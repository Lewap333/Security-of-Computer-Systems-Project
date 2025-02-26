#!/bin/bash

# Wprowadzenie hasła z ukrytym wpisywaniem
read -sp "Enter passphrase: " PASSPHRASE
echo 

echo "Generating private key.."
openssl genrsa -aes256 \
    -passout pass:"$PASSPHRASE" \
    -out private_key.pem 4096

echo "Generating public key.."
openssl rsa \
    -passin pass:"$PASSPHRASE" \
    -in private_key.pem \
    -pubout \
    -out public_key.pem
