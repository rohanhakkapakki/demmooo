import time
from scapy.all import sniff, IP

# No error messages, no indices, just the monitor
def monitor(pkt):
    if IP in pkt:
        size = len(pkt)
        
        # Behavior check: Rogue attacks use max-size packets (1400B+)
        if size > 1350:
            status = "🔴 ALERT: ROGUE ATTACK DETECTED"
        else:
            status = "🟢 STATUS: SAFE"
            
        print(f"[{time.strftime('%H:%M:%S')}] {status} | Size: {size}B")

# Start background sniffing immediately
sniff(prn=monitor, store=0)