import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase2_asymmetric.dh_exchange import DHParticipant
from cryptography.hazmat.primitives.asymmetric import dh

def simulate_mitm():
    print("\n[Phase 2 - MITM Attack on DH]")
    parameters = dh.generate_parameters(generator=2, key_size=512)
    
    alice = DHParticipant(parameters)
    bob = DHParticipant(parameters)
    eve = DHParticipant(parameters)
    
    alice_secret = alice.generate_shared_secret(eve.public_key)
    bob_secret = bob.generate_shared_secret(eve.public_key)
    
    eve_secret_with_alice = eve.generate_shared_secret(alice.public_key)
    eve_secret_with_bob = eve.generate_shared_secret(bob.public_key)
    
    print(f"University derived secret (hex): {alice_secret.hex()}")
    print(f"Student derived secret (hex):    {bob_secret.hex()}")
    
    print(f"Eve's secret with Uni (hex):     {eve_secret_with_alice.hex()}")
    print(f"Eve's secret with Student (hex): {eve_secret_with_bob.hex()}")
    
    print("\nResult: University and Student have different secrets, but Eve shares a secret with both.")
    print("Fix: Authenticated DH. Parties must sign their public keys.")

if __name__ == "__main__":
    simulate_mitm()
