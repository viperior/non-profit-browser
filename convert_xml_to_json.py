import json
import sys
import xmltodict

def convert_xml_to_json(source_xml_file_path, target_json_file_path):
    with open(source_xml_file_path, 'r') as source_xml_file:
        xml_file_data = source_xml_file.read()
        xml_dict = xmltodict.parse(xml_file_data)
        json_data = json.dumps(xml_dict)
        
        with open(target_json_file_path, 'w') as target_json_file:
            target_json_file.write(json_data)
