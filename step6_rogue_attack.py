import socket
import time

# Target the Windows Hotspot Gateway
TARGET_IP = "192.168.137.1" 
PORT = 8080

print("💀 ROGUE ATTACK INITIATED...")
print("Blasting heavy packets to trigger the Sentinel!")

# This payload is 2500 bytes (spikes AvgSize above the 900B threshold)
malicious_payload = b"MALICIOUS_DATA_EXFILTRATION_TEST_" * 80 

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        # High-speed flood to trigger the 'Total Packets' threshold
        sock.sendto(malicious_payload, (TARGET_IP, PORT))
        time.sleep(0.01) # Small delay to prevent crashing your card
except KeyboardInterrupt:
    print("\nAttack Stopped.")