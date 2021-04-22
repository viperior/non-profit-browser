import xml.etree.ElementTree as ET
import xmltodict

class ReturnFiling:
    def __init__(self, form_file_name, form_path):
        self.form_file_name = form_file_name
        self.return_s3_doc_id = form_file_name.replace('_public.xml', '')
        self.form_path = form_path
        self.return_data_dict = self.get_return_data_dict()

    def display_contents(self):
        print(self.form_file_name)
        print('EIN: ', self.get_return_ein())
        print('Name: ', self.get_return_filer_name_full())
        print('Address: ', self.get_return_filer_address_full())
        print('File: ', self.form_file_name)
        print('===')

    def get_return_data(self):
        return self.return_data_dict['ns0:Return']

    def get_return_data_dict(self):
        return dict(xmltodict.parse(self.get_xml_string()))

    def get_return_ein(self):
        return self.get_return_filer()['ns0:EIN']

    def get_return_filer(self):
        return self.get_return_header()['ns0:Filer']

    def get_return_filer_address(self):
        return self.get_return_filer()['ns0:USAddress']

    def get_return_filer_address_full(self):
        return_string = ''
        return_filer_address = self.get_return_filer_address()
        return_filer_address_keys = return_filer_address.keys()

        values_to_add = [
            'ns0:AddressLine1',
            'ns0:AddressLine2',
            'ns0:City',
            'ns0:State',
            'ns0:ZIPCode'
        ]

        for i, value in enumerate(values_to_add):
            if value in return_filer_address_keys:
                return_string += return_filer_address[value]

                if i < len(values_to_add) - 1:
                    return_string += ', '
        
        return return_string

    def get_return_filer_name(self):
        return self.get_return_filer()['ns0:Name']

    def get_return_filer_name_full(self):
        return_filer_name = self.get_return_filer_name()
        return_string = self.get_return_filer_name()['ns0:BusinessNameLine1']

        if 'ns0:BusinessNameLine2' in return_filer_name.keys():
            return_string += ' ' + str(return_filer_name['ns0:BusinessNameLine2'])

        return return_string

    def get_return_header(self):
        return self.get_return_data()['ns0:ReturnHeader']

    def get_xml_data(self):
        return self.get_xml_tree().getroot()

    def get_xml_string(self):
        return ET.tostring(self.get_xml_data(), encoding='utf-8', method='xml')

    def get_xml_tree(self):
        return ET.parse(self.form_path)
