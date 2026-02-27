import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

print("1. Waking up the trained AI Model...")
# Load the model and scaler we created in Step 3
model = pickle.load(open('trained_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

print("2. Loading test devices into the network...")
# Load your real, safe device
real_df = pd.read_csv('iot_fingerprints.csv')

# Recreate the hacker's rogue device to test the system
rogue_data = {
    'device_ip': ['192.168.1.999 (Rogue)'],
    'avg_packet_size': [4500.5],
    'std_packet_size': [2100.0],
    'total_packets': [1500],
    'num_protocols': [8],
    'external_ips': [25],
    'tcp_ratio': [0.95],
    'udp_ratio': [0.05]
}
rogue_df = pd.DataFrame(rogue_data)

# Combine them so the AI can inspect both
test_data = pd.concat([real_df, rogue_df], ignore_index=True)
device_ips = test_data['device_ip'].tolist()

# Drop the IP column so the AI only sees the math
X_test = test_data.drop(columns=['device_ip'])
X_test_scaled = scaler.transform(X_test)

print("3. Scanning network traffic...\n")
# The AI makes its prediction! (0 = SAFE, 1 = ROGUE)
predictions = model.predict(X_test_scaled)

print("🚨 === REAL-TIME DETECTION RESULTS === 🚨")
for i in range(len(predictions)):
    status = "✅ SAFE DEVICE ALLOWED" if predictions[i] == 0 else "🛑 ROGUE DEVICE BLOCKED!"
    print(f"Device IP: {device_ips[i]}")
    print(f"Status:    {status}\n")


print("4. Generating Hackathon Presentation Graphs...")

# --- GRAPH 1: Network Behavior Scatter Plot ---
plt.figure(figsize=(10, 6))
colors = ['green' if p == 0 else 'red' for p in predictions]
sizes = [200 if p == 0 else 600 for p in predictions]
markers = ['o' if p == 0 else 'X' for p in predictions]

for i in range(len(test_data)):
    plt.scatter(test_data['avg_packet_size'].iloc[i], 
                test_data['total_packets'].iloc[i], 
                c=colors[i], s=sizes[i], marker=markers[i], 
                edgecolors='black', alpha=0.8,
                label=f"{device_ips[i]} ({'Safe' if predictions[i]==0 else 'Rogue'})")

plt.title('IoT Device Network Behavior Analysis', fontsize=14, fontweight='bold')
plt.xlabel('Average Packet Size (Bytes)', fontsize=12, fontweight='bold')
plt.ylabel('Total Packets Sent', fontsize=12, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend()
plt.savefig('graph1_behavior_scatter.png', dpi=300, bbox_inches='tight')
print("✅ Saved Graph 1: graph1_behavior_scatter.png")

# --- GRAPH 2: Security Risk Bar Chart ---
plt.figure(figsize=(8, 5))
plt.bar(device_ips, test_data['external_ips'], color=colors, edgecolor='black', alpha=0.8)
plt.title('Security Risk: External Server Connections', fontsize=14, fontweight='bold')
plt.ylabel('Number of External Servers Contacted', fontsize=12, fontweight='bold')
plt.grid(True, axis='y', linestyle='--', alpha=0.3)
plt.savefig('graph2_security_risk.png', dpi=300, bbox_inches='tight')
print("✅ Saved Graph 2: graph2_security_risk.png")

print("\n🎉 SYSTEM PROTOTYPE 100% COMPLETE! 🎉")