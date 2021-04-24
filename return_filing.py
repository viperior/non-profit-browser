import requests
import xml.etree.ElementTree as ET
import xmltodict

class ReturnFiling:
    def __init__(self, form_file_name, form_path=None):
        self.form_file_name = form_file_name
        self.return_s3_doc_id = int(form_file_name.replace('_public.xml', ''))
        self.form_path = form_path
        self.load_method = self.get_load_method()
        self.return_data_dict = self.get_return_data_dict()
        self.database_payload = self.get_database_payload()

    def display_contents(self):
        print('EIN: ', self.get_return_filer_ein())
        print('Name: ', self.get_return_filer_name_full())
        print('Address: ', self.get_return_filer_address_full())
        print('File: ', self.form_file_name)
        print('Return version: ', self.get_return_version())
        print('===')

    def get_database_payload(self):
        payload = {
            "form_file_name": self.form_file_name,
            "return_s3_doc_id": self.return_s3_doc_id,
            "return_version": self.get_return_version(),
            "ein": self.get_return_filer_ein(),
            "return_filer_name": self.get_return_filer_name_full(),
            "total_assets": self.get_total_assets_eoy()
        }
        return payload

    def get_load_method(self):
        if self.form_path == None:
            method = 's3'
        else:
            method = 'file'

        return method
        
    def get_return_data(self):
        return self.return_data_dict['ns0:Return']

    def get_return_data_dict(self):
        return dict(xmltodict.parse(self.get_xml_string()))

    def get_return_filer_ein(self):
        return self.get_return_filer()['ns0:EIN']

    def get_return_filer(self):
        return self.get_return_header()['ns0:Filer']

    def get_return_filer_address(self):
        return_filer = self.get_return_filer()

        if 'ns0:USAddress' in return_filer.keys():
            return self.get_return_filer()['ns0:USAddress']
        elif 'ns0:ForeignAddress' in return_filer.keys():
            return self.get_return_filer()['ns0:ForeignAddress']
        else:
            print('[ERROR] Could not find keys, ns0:USAddress or ns0:ForeignAddress, in file: ', self.form_file_name)
            print(return_filer.keys())
            return 'Address Not Found'
        
    def get_return_filer_address_full(self):
        return_string = ''
        return_filer_address = self.get_return_filer_address()

        values_to_add = [
            'ns0:AddressLine1',
            'ns0:AddressLine2',
            'ns0:City',
            'ns0:State',
            'ns0:ZIPCode'
        ]

        for i, value in enumerate(values_to_add):
            if value in return_filer_address.keys():
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

    def get_return_version(self):
        return self.get_return_data()['@returnVersion']

    def get_total_assets_eoy(self):
        return_data = self.get_return_data()['ns0:ReturnData']

        form_types = [
            '990',
            '990EZ',
            '990PF'
        ]

        for form_type in form_types:
            form_key = f"ns0:IRS{form_type}"

            if form_key in return_data.keys():
                form = return_data[form_key]

        total_asset_keys = [
            'ns0:TotalAssetsEOY',
            'ns0:TotalAssets',
            'ns0:FMVAssetsEOY'
        ]

        for key in total_asset_keys:
            if key in form.keys():
                total_assets = form[key]
                
                if isinstance(total_assets, dict):
                    if 'ns0:EOY' in total_assets.keys():
                        total_assets = total_assets['ns0:EOY']
                    
                break

        return total_assets

    def get_xml_data(self):
        return self.get_xml_tree()

    def get_xml_string(self):
        return ET.tostring(self.get_xml_data(), encoding='utf-8', method='xml')

    def get_xml_tree(self):
        if self.load_method == 'file':
            xml_tree = ET.parse(self.form_path).getroot()
        elif self.load_method == 's3':
            url = (
                f"https://s3.amazonaws.com/irs-form-990/"
                f"{self.form_file_name}"
            )
            r = requests.get(url)
            xml_tree = ET.fromstring(r.content)
        else:
            print(f"[ERROR] Unhandled load method: {self.load_method}")

        return xml_tree
