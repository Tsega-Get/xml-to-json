import xml.etree.ElementTree as ET
import json
import math

def xml_to_json(xml_file, output_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Convert XML to a Python dictionary
    xml_dict = xml_to_dict(root)
    
    # Save JSON data to file
    with open(output_file, "w") as json_file:
        json.dump(xml_dict, json_file, indent=4)

def get_element_text(element, path):
    found_element = element.find(path)
    if found_element is not None:
        return found_element.text.strip()
    return None

def process_numeric_part(numeric_part, prefix, part):
    numeric_part = ''.join(filter(str.isdigit, numeric_part))
    if not numeric_part:
        return None
    if prefix:
        numeric_part = prefix.strip() + numeric_part
    suffix = ''.join(filter(str.isalpha, part))
    return numeric_part + suffix if suffix else numeric_part

def process_designation_part(part):
    prefix = ""
    if "RWY" in part:
        prefix, part = part.split("RWY")
    part = part.strip()  # Remove leading/trailing spaces
    numeric_parts = [p.strip() for p in part.split("-")]
    return [process_numeric_part(numeric_part, prefix, part) for numeric_part in numeric_parts]

def get_rwy_data(rwy):
    rwy_data = []
    txt_desig = get_element_text(rwy, './RwyUid/txtDesig')
    if txt_desig is None or txt_desig.strip() == "RWY":
        return rwy_data  # Return empty rwy_data if txt_desig is None or "RWY"
    
    # Extracting runway designation numbers
    designation_parts = txt_desig.split('/')
    runway_designation_numbers = [number for part in designation_parts for number in process_designation_part(part) if number]
    for runway_designation_number in runway_designation_numbers:
        rwy_data.append({
            "runway_designation_number": runway_designation_number,
            "landing_distance_available": "",
            "landing_distance_unit": ""
        })

    return rwy_data
def xml_to_dict(element):
    xml_dict = {}
    for rwy in element.findall('.//Rwy'):
        code_id = get_element_text(rwy, './RwyUid/AhpUid/codeId')
        if code_id is None:
            code_id = get_element_text(rwy, './RwyUid/codeId')  # Try fetching directly
        if code_id is not None:
            rwy_data = get_rwy_data(rwy)
            xml_dict.setdefault(code_id, []).extend(rwy_data)
    return xml_dict

# Path to the XML file
xml_file = 'DB_rwy_runway_xml.xml'

# Output file name
output_file = 'DB_rwy_runway.json'

# Convert XML to JSON and save to file
xml_to_json(xml_file, output_file)