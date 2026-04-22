import json
import os

base_path = r'C:\Users\manik\.gemini\antigravity\brain\a4d5fccf-f834-4f3b-b98b-72ba2ad5eb1d\scratch'
batch3_path = os.path.join(base_path, 'batch3.json')

with open(batch3_path, 'r') as f:
    batch3 = json.load(f)

q = batch3[0]
a = batch3[1]
e = batch3[2]

chunk_size = 20
for i in range(0, len(q), chunk_size):
    chunk_idx = i // chunk_size
    chunk = [q[i:i+chunk_size], a[i:i+chunk_size], e[i:i+chunk_size]]
    with open(os.path.join(base_path, f'batch3_chunk{chunk_idx}.json'), 'w') as f:
        json.dump(chunk, f)
