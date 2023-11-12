# pip install pycryptodome opencv-python
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# Function to pad data
def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def main():
    # Ask user for the image path
    image_path = input("Enter path to image: ")
    image_path = r"{}".format(image_path)  # Convert to raw string
    image = cv2.imread(image_path)


    if image is None:
        print("Error: Image not found. Please check the file path.")
        return

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

if __name__ == "__main__":
    main()

