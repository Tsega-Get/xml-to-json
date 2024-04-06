import json

def merge_items(item_a, item_b):
    merged_item = item_a.copy()
    if item_a['landing_distance_available'] != "":
        merged_item['landing_distance_available'] = item_a['landing_distance_available']
        merged_item['landing_distance_unit'] = item_a['landing_distance_unit']
    else:
        merged_item['landing_distance_available'] = item_b['landing_distance_available']
        merged_item['landing_distance_unit'] = item_b['landing_distance_unit']
    return merged_item

def merge_lists(list_a, list_b, key):
    merged_list = []
    for item_a in list_a:
        for item_b in list_b:
            if item_a[key] == item_b[key]:
                merged_item = merge_items(item_a, item_b)
                merged_list.append(merged_item)
                break
        else:
            merged_list.append(item_a)
    for item_b in list_b:
        if item_b[key] not in [item[key] for item in merged_list]:
            merged_list.append(item_b)
    return merged_list

def merge_json(json_a, json_b, key):
    merged_json = {}

    for k, v in json_a.items():
        if k in json_b:
            merged_json[k] = merge_lists(v, json_b[k], key)
        else:
            merged_json[k] = v

    for k, v in json_b.items():
        if k not in merged_json:
            merged_json[k] = v

    return merged_json
# Load JSON files
with open('DB_rdd_runway.json', 'r') as file:
    json_a = json.load(file)

with open('DB_rwy_runway.json', 'r') as file:
    json_b = json.load(file)

# Define the common key
common_key = "runway_designation_number"

# Merge JSON files
merged_json = merge_json(json_a, json_b, common_key)

# Write merged JSON to a new file
with open('DB_merged_runway.json', 'w') as file:
    json.dump(merged_json, file, indent=4)
