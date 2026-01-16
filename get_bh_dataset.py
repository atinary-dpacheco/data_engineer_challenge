# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "ord-schema",
#     "protobuf",
# ]
# ///

import json
import os
import urllib.request

from google.protobuf.json_format import MessageToDict
from ord_schema.message_helpers import load_message, write_message
from ord_schema.proto import dataset_pb2

# Map of dataset folder name to binary URL
datasets = {
    "AstraZeneca_ELN": "https://github.com/open-reaction-database/ord-data/raw/main/data/00/ord_dataset-00005539a1e04c809a9a78647bea649c.pb.gz",
    "Merck_HTE": "https://github.com/open-reaction-database/ord-data/raw/main/data/cb/ord_dataset-cbcc4048add7468e850b6ec42549c70d.pb.gz",
}

combined_dataset = dataset_pb2.Dataset()
combined_dataset.name = "Mixed Buchwald-Hartwig Subset for Interview"

for name, url in datasets.items():
    print(f"Downloading {name}...")
    temp_file = f"{name}.pb.gz"
    try:
        urllib.request.urlretrieve(url, temp_file)
        # Load and take 10 reactions from each to ensure variety
        ds = load_message(temp_file, dataset_pb2.Dataset)
        combined_dataset.reactions.extend(ds.reactions[:10])
        print(f"  Successfully added 10 reactions from {name}")
        os.remove(temp_file)  # Clean up
    except Exception as e:
        print(f"  Error processing {name}: {e}")

# Save the unified binary file
pb_output = "ord_challenge_subset.pb.gz"
write_message(combined_dataset, pb_output)

# Convert protobuf to JSON-serializable dict and save
json_output = "ord_challenge_subset.json"
dataset_dict = MessageToDict(combined_dataset, preserving_proto_field_name=True)
with open(json_output, "w") as f:
    json.dump(dataset_dict, f, indent=2)

print(f"\nSuccess! '{pb_output}' and '{json_output}' are ready for the candidate.")