import os
import xml.dom.minidom
import xml.etree.ElementTree as ET
import xmltodict

class ReturnFiling:
    def __init__(self, form_file_name, form_path):
        self.form_file_name = form_file_name
        self.return_s3_doc_id = form_file_name.replace('_public.xml', '')
        self.form_path = form_path
        self.xml_tree = ET.parse(form_path)
        self.xml_data = self.xml_tree.getroot()
        self.xml_str = ET.tostring(self.xml_data, encoding='utf-8', method='xml')
        self.return_data_dict = dict(xmltodict.parse(self.xml_str))
        self.return_data = self.return_data_dict['ns0:Return']
        self.return_header = self.return_data['ns0:ReturnHeader']
        self.return_filer = self.return_header['ns0:Filer']
        self.return_filer_name = self.return_filer['ns0:Name']
        self.return_ein = self.return_filer['ns0:EIN']
        self.return_filer_name_full = self.get_return_filer_name_full()

    def display_contents(self):
        print(self.form_file_name)
        print('EIN: ', self.return_ein)
        print('Name: ', self.return_filer_name_full)
        print('===')

    def get_return_filer_name_full(self):
        return_string = self.return_filer_name['ns0:BusinessNameLine1']

        if 'ns0:BusinessNameLine2' in self.return_filer_name.keys():
            return_string += ' ' + str(self.return_filer_name['ns0:BusinessNameLine2'])

        return return_string
        
def main():
    limit = 5
    directory = 'data\\indices'
    file_list = os.scandir(directory)

    for index, form_path in enumerate(file_list):
        if index > limit:
            break
        else:
            full_form_path = directory + "\\" + form_path.name
            current_return = ReturnFiling(form_path.name, full_form_path)
            current_return.display_contents()

main()
