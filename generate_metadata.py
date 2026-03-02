import os
import csv

root_dir = "humanai/dataset"
transcription_file = os.path.join(root_dir, "usma-prompts.txt")
output_csv = os.path.join(root_dir, "metadata.csv")

# Step 1: Read transcription file
id_to_text = {}

with open(transcription_file, "r", encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        utt_id = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        id_to_text[utt_id] = text

# Step 2: Create metadata rows
rows = []

for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)

    if not os.path.isdir(folder_path):
        continue

    for file in os.listdir(folder_path):
        if file.endswith(".wav"):
            utt_id = file.replace(".wav", "")

            if utt_id not in id_to_text:
                print(f"Warning: {utt_id} not found in transcription file")
                continue

            full_path = os.path.abspath(os.path.join(folder_path, file))

            rows.append({
                "path": full_path,
                "text": id_to_text[utt_id],
                "utterance_id": utt_id
            })

# Step 3: Write CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["path", "text", "utterance_id"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Metadata file created at {output_csv}")
print(f"Total samples: {len(rows)}")