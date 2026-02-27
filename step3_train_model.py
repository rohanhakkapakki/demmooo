import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import pickle

print("1. Loading real device fingerprint...")
# Load the real fingerprint you just extracted
real_df = pd.read_csv('iot_fingerprints.csv')

# Assign a label: 0 means "KNOWN/SAFE", 1 means "ROGUE"
real_df['label'] = 0

print("2. Generating simulated Rogue Device to teach the AI...")
# We create a fake device that behaves like a hacker exfiltrating data
rogue_data = {
    'device_ip': ['192.168.1.999'],      # Fake IP
    'avg_packet_size': [4500.5],         # Massive packets (stealing data)
    'std_packet_size': [2100.0],         # Highly erratic behavior
    'total_packets': [1500],             # Sending way too much data
    'num_protocols': [8],                # Trying to attack different ports
    'external_ips': [25],                # Connecting to 25 random servers
    'tcp_ratio': [0.95],                 # Maintaining persistent connections
    'udp_ratio': [0.05],
    'label': [1]                         # 1 = ROGUE / THREAT
}
rogue_df = pd.DataFrame(rogue_data)

# Combine your real data and the fake rogue data into one training set
training_data = pd.concat([real_df, rogue_df], ignore_index=True)

print("3. Preparing math features for the ML Model...")
# The AI only looks at the math, so we drop the IP and the Label columns
X = training_data.drop(columns=['device_ip', 'label'])
y = training_data['label']

# Scale the data (Crucial step! It makes sure big numbers don't overpower small ones)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("4. Training the K-Nearest Neighbors AI...")
# We use K=1 here because our dataset is small for the prototype
model = KNeighborsClassifier(n_neighbors=1) 
model.fit(X_scaled, y)

print("5. Saving the trained AI 'brain'...")
# Save the model and scaler so we can use them later to test new devices
pickle.dump(model, open('trained_model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))

print("\n✅ SUCCESS: AI Model trained and saved as 'trained_model.pkl'!")