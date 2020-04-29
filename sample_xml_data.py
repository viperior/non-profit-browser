import os
import xml.dom.minidom

data_directory = './data/990/'

for index, file in enumerate(os.listdir(data_directory)):
    file_path = data_directory + file
    print(file)
    dom = xml.dom.minidom.parse(file_path)
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)
    
    if index >= 2:
        break
