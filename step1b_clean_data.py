import pandas as pd
import numpy as np

print("Reading raw Wireshark data...")

# Load the raw CSV you just exported
df = pd.read_csv('wireshark_raw.csv')

# Create a fresh, clean table for the ML model
clean_df = pd.DataFrame()

# 1. Map Wireshark's columns to match our ML model's expected names
clean_df['timestamp'] = df['Time']
clean_df['src_ip'] = df['Source']
clean_df['dst_ip'] = df['Destination']
clean_df['protocol'] = df['Protocol']
clean_df['packet_size'] = df['Length']

# 2. Inject the missing variables our model expects
# We will generate a fake connection duration between 0.1 and 2 seconds
clean_df['duration_sec'] = np.random.uniform(0.1, 2.0, len(df)) 
clean_df['device_name'] = 'Real_Test_Phone'

# 3. Guess the behavior based on the protocol
def guess_behavior(proto):
    if proto in ['TCP', 'TLSv1.2', 'QUIC']:
        return 'device_sync'
    elif proto in ['UDP']:
        return 'health_monitoring'
    else:
        return 'background_noise'

clean_df['behavior_type'] = df['Protocol'].apply(guess_behavior)

# Save the perfectly formatted data!
clean_df.to_csv('smartwatch_traffic.csv', index=False)
print("✅ SUCCESS: Data cleaned and saved as 'smartwatch_traffic.csv'!")