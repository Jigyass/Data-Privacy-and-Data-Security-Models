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

# Alice's matrix A (5x8)
A = np.random.randint(low=0, high=10, size=(5, 8))
print("Alice's Matrix A:")
print(A)

# Alice's server setup
host = 'localhost'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print("Alice's Server Started. Waiting for Connection...")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)

        # For 512-bit key
        public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)
        # Send public key to Bob
        conn.send(pickle.dumps(public_key))

        # Receive encrypted matrix from Bob
        encrypted_matrix = pickle.loads(receive_complete_message(conn))

        # Perform matrix multiplication
        C = np.empty([5, 4], dtype=object)
        for i in range(5):
            for j in range(4):
                sum = public_key.encrypt(0)
                for k in range(8):
                    sum += encrypted_matrix[k][j] * int(A[i][k])
                C[i][j] = sum

        # Decrypt the result
        decrypted_C = np.zeros([5, 4])
        for i in range(5):
            for j in range(4):
                decrypted_C[i][j] = private_key.decrypt(C[i][j])

        # Print the last ciphertext (right before decryption)
        print("Last Ciphertext (Encrypted Matrix C):")
        print(C)

        # Print the decrypted product A x B
        print("Decrypted Product (A x B):")
        print(decrypted_C)

        # Send the result back to Bob
        conn.send(pickle.dumps(decrypted_C))
        print("Sending decrypted result to Bob.")


