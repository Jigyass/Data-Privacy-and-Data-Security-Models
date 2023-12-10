# pip install pycryptodome opencv-python
import os
import numpy as np
from Crypto.Cipher import AES
import cv2

def unpad(data):
    return data.rstrip(b"\0")

def main():
    current_dir = os.getcwd()

    # Check if required files exist
    required_files = ['encrypted_data.bin', 'key.bin', 'iv.bin', 'image_shape.txt']
    missing_files = [file for file in required_files if not os.path.exists(os.path.join(current_dir, file))]

    if missing_files:
        print("Error: Missing required files:", ', '.join(missing_files))
        return

    # Load encrypted data, key, iv, and shape
    with open(os.path.join(current_dir, 'encrypted_data.bin'), 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    with open(os.path.join(current_dir, 'key.bin'), 'rb') as key_file:
        key = key_file.read()
    with open(os.path.join(current_dir, 'iv.bin'), 'rb') as iv_file:
        iv = iv_file.read()
    with open(os.path.join(current_dir, 'image_shape.txt'), 'r') as shape_file:
        shape_str = shape_file.read()
    original_shape = tuple(map(int, shape_str.split(',')))

    # Decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data))

    # Convert decrypted data back to image
    image_array = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(original_shape)

    # Save the image
    output_image_path = os.path.join(current_dir, 'decrypted_image.jpg')
    cv2.imwrite(output_image_path, image_array)

    print("Decryption complete. Image saved as:", output_image_path)

if __name__ == "__main__":
    main()

