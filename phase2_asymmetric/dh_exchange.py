from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os

class DHParticipant:
    def __init__(self, parameters):
        self.private_key = parameters.generate_private_key()
        self.public_key = self.private_key.public_key()
        
    def generate_shared_secret(self, peer_public_key):
        shared_key = self.private_key.exchange(peer_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=16,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
        return derived_key

def simulate_dh():
    print("[Phase 2 - Diffie-Hellman Key Exchange]")
    parameters = dh.generate_parameters(generator=2, key_size=512)
    
    university = DHParticipant(parameters)
    student = DHParticipant(parameters)
    
    uni_secret = university.generate_shared_secret(student.public_key)
    student_secret = student.generate_shared_secret(university.public_key)
    
    print(f"University derived secret (hex): {uni_secret.hex()}")
    print(f"Student derived secret (hex):    {student_secret.hex()}")
    assert uni_secret == student_secret
    print("Keys match! Secure channel established.")
    return parameters, university, student

if __name__ == "__main__":
    simulate_dh()
