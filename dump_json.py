import json

# Read the JSON file
with open('DB_merged_runway.json', 'r') as file:
    data = json.load(file)

# Dump the JSON data back to the file with minimized formatting
with open('DB_dumped_runway.json', 'w') as file:
    json.dump(data, file, separators=(',', ':'))