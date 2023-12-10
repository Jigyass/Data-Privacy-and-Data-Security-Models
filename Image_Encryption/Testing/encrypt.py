# pip install pycryptodome opencv-python
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import argparse

# Function to pad data
def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not found at path:", image_path)
        return False

    print("Image loaded successfully")

    # Convert image to encryptable format
    image_bytes = image.tobytes()
    # Save original shape and color channels
    original_shape = image.shape

    # Generate key and initialization vector
    key = get_random_bytes(16)  # AES key should be 16, 24, or 32 bytes long
    iv = get_random_bytes(AES.block_size)  # Initialization vector

    # Encrypt the image
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(image_bytes)
    encrypted_data = cipher.encrypt(padded_data)

    # Save the encrypted data, key, iv, and shape in the current directory
    current_dir = os.getcwd()
    with open(os.path.join(current_dir, 'encrypted_data.bin'), 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    with open(os.path.join(current_dir, 'key.bin'), 'wb') as key_file:
        key_file.write(key)
    with open(os.path.join(current_dir, 'iv.bin'), 'wb') as iv_file:
        iv_file.write(iv)
    with open(os.path.join(current_dir, 'image_shape.txt'), 'w') as shape_file:
        shape_file.write(','.join(map(str, original_shape)))

    print("Encryption complete. Files saved in:", current_dir)
    return True

def main():
    parser = argparse.ArgumentParser(description="Encrypt an image file.")
    parser.add_argument("image_path", help="Path to the image file to encrypt")
    args = parser.parse_args()

    encrypt_image(args.image_path)

if __name__ == "__main__":
    main()
