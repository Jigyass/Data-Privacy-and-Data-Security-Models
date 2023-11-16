import socket
import numpy as np
from phe import paillier
import pickle

def receive_complete_message(connection):
    data = b''
    while True:
        part = connection.recv(4096)
        data += part
        if len(part) < 4096:
            # Either 0 or end of data
            break
    return data

# Bob's client setup
host = 'localhost'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print("Connected to Alice's Server")

    # Receive public key from Alice
    public_key = pickle.loads(s.recv(4096))

    # Define Bob's matrix B (8x4)
    B = np.random.randint(low=0, high=10, size=(8, 4))
    print("Bob's Matrix B:")
    print(B)

    # Blinding the matrix with a factor of 4
    B_blinded = B * 4

    # Encrypting the blinded matrix
    encrypted_B_blinded = np.array([[public_key.encrypt(int(b)) for b in row] for row in B_blinded])

    # Print the encrypted blinded matrix B
    print("Encrypted Blinded Matrix B:")
    print(encrypted_B_blinded)

    # Send the encrypted blinded matrix to Alice
    s.send(pickle.dumps(encrypted_B_blinded))

    # Receive the decrypted and multiplied result from Alice
    decrypted_result = pickle.loads(receive_complete_message(s))

    # Correct the result by dividing by the blinding factor
    final_result = decrypted_result / 4

    print("Final Result (Product of A and B):")
    print(final_result)

