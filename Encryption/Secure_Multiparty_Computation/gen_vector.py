import random

def generate_boolean_vector(length=10):
    return [random.choice([0, 1]) for _ in range(length)]

alice_vector = generate_boolean_vector()
bob_vector = generate_boolean_vector()

# Writing vectors to files
with open('alice_vector.txt', 'w') as file:
    file.write(' '.join(map(str, alice_vector)))

with open('bob_vector.txt', 'w') as file:
    file.write(' '.join(map(str, bob_vector)))

