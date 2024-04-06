import xml.etree.ElementTree as ET
import json
import math

def xml_to_json(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Convert XML to a Python dictionary
    xml_dict = xml_to_dict(root)
    
    # Convert the dictionary to JSON
    json_data = xml_to_json_format(xml_dict)
    
    # Save JSON data to file
    with open("DB_rdd_runway.json", "w") as json_file:
        json_file.write(json_data)

def get_element_text(element, path):
    found_element = element.find(path)
    if found_element is not None:
        return found_element.text.strip()
    return None

def get_rdd_data(rdd):
    rdd_data = {}
    txt_desig = get_element_text(rdd, './/RdnUid/txtDesig')
    if txt_desig is not None:
        rdd_data['runway_designation_number'] = txt_desig
    val_dist = get_element_text(rdd, './/valDist')
    if val_dist is not None:
        rdd_data['landing_distance_available'] = int(math.floor(float(val_dist)))
    uom_dist = get_element_text(rdd, './/uomDist')
    if uom_dist is not None:
        rdd_data['landing_distance_unit'] = uom_dist
    return rdd_data

def xml_to_dict(element):
    xml_dict = {}
    for rdd in element.findall('.//Rdd'):
        code_type = get_element_text(rdd, './/codeType')
        if code_type == "LDA": # Check if codeType is "LDA" incase of runway data there will be multiple codeType like "TORA", "TODA", "ASDA", "LDA"
            code_id = get_element_text(rdd, './/codeId')
            if code_id:
                rdd_data = get_rdd_data(rdd)
                xml_dict.setdefault(code_id, []).append(rdd_data)
    return xml_dict

def xml_to_json_format(xml_dict):
    # Convert XML dictionary to the required JSON format
    json_data = json.dumps(xml_dict, indent=4)
    return json_data

# Path to the XML file
xml_file = 'DB_rdd_runway_xml.xml'

# Convert XML to JSON and save to file
xml_to_json(xml_file)
