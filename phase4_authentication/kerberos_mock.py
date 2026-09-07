import time

def simulate_kerberos_gate(student_id):
    print("\n[Phase 4 - Kerberos Authentication Gate]")
    print(f"1. Client (Student {student_id}) requests Ticket Granting Ticket (TGT) from Authentication Server (AS).")
    time.sleep(0.5)
    print("2. AS verifies Student identity in database and issues encrypted TGT.")
    time.sleep(0.5)
    print("3. Client sends TGT to Ticket Granting Server (TGS) requesting access to Transcript Service.")
    time.sleep(0.5)
    print("4. TGS verifies TGT, issues Service Ticket for Transcript Service.")
    time.sleep(0.5)
    print("5. Client presents Service Ticket to Transcript Server.")
    time.sleep(0.5)
    print("6. Transcript Server verifies Service Ticket. Access GRANTED.")
    return True

if __name__ == "__main__":
    simulate_kerberos_gate("987654321")
