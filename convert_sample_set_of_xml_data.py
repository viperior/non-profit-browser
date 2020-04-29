import convert_xml_to_json
import os

source_xml_data_directory = './data/990/'
target_json_data_directory = './data/990/json/'
number_of_files_to_convert = 2
print('Converting ' + str(number_of_files_to_convert) + ' files...')

for index, source_xml_file_name in enumerate(os.listdir(source_xml_data_directory)):
    if index + 1 > number_of_files_to_convert:
        break
    
    source_xml_file_path = source_xml_data_directory + source_xml_file_name
    target_json_file_name = source_xml_file_name.replace('.xml', '.json')
    target_json_file_path = target_json_data_directory + target_json_file_name
    print(source_xml_file_path + ' > ' + target_json_file_path)
    convert_xml_to_json.convert_xml_to_json(source_xml_file_path, target_json_file_path)
