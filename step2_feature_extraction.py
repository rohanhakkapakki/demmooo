import pandas as pd
import numpy as np

class IoTDeviceFingerprinter:
    def __init__(self, csv_file):
        # We are now reading the raw Wireshark file directly!
        self.df = pd.read_csv(csv_file)
    
    def extract_features(self):
        print("Extracting behavioral features from network traffic...")
        fingerprints = []
        
        # Group by device IP (Wireshark calls this 'Source')
        for device_ip in self.df['Source'].unique():
            traffic = self.df[self.df['Source'] == device_ip]
            
            # Extract features using Wireshark's exact column names
            features = {
                'device_ip': device_ip,
                
                # Packet size features (Wireshark calls this 'Length')
                'avg_packet_size': traffic['Length'].mean(),
                'std_packet_size': traffic['Length'].std(),
                
                # Volume features
                'total_packets': len(traffic),
                
                # Protocol features (Wireshark calls this 'Protocol')
                'num_protocols': traffic['Protocol'].nunique(),
                
                # Connection features (Wireshark calls this 'Destination')
                'external_ips': len([ip for ip in traffic['Destination'].unique() 
                                     if not str(ip).startswith('192.168') and not str(ip).startswith('10.') and not str(ip).startswith('172.')]),
                
                # Protocol usage ratios
                'tcp_ratio': (traffic['Protocol'].isin(['TCP', 'TLSv1.2', 'HTTP', 'HTTPS'])).sum() / len(traffic),
                'udp_ratio': (traffic['Protocol'].isin(['UDP', 'QUIC', 'DNS'])).sum() / len(traffic),
            }
            
            fingerprints.append(features)
        
        return pd.DataFrame(fingerprints)

if __name__ == "__main__":
    # Ensure this exactly matches the name of your file!
    extractor = IoTDeviceFingerprinter('wireshark_raw.csv')
    fingerprints_df = extractor.extract_features()
    
    print("\n📊 Extracted Device Fingerprints:\n")
    print(fingerprints_df.to_string(index=False))
    
    # Save the fingerprints for the Machine Learning model
    fingerprints_df.to_csv('iot_fingerprints.csv', index=False)
    print("\n✅ SUCCESS: Fingerprints saved to 'iot_fingerprints.csv'")
    