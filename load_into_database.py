import os
import traceback
import xml.dom.minidom
import xml.etree.ElementTree as ET
import xmltodict

def get_return_filer_name(xml_str):
    data_dict = dict(xmltodict.parse(xml_str))
    return_data = data_dict['ns0:Return']
    return_header = return_data['ns0:ReturnHeader']
    return_filer = return_header['ns0:Filer']
    return_filer_name = return_filer['ns0:Name']['ns0:BusinessNameLine1']

    return return_filer_name

def get_return_keys(json):
    return json.keys()

def store_form_to_db(payload):
    print(payload)

def main():
    directory = 'data\\indices'
    file_list = os.scandir(directory)
    
    for index, form in enumerate(file_list):
        if index > 50:
            break
        else:
            form_file_name = form.name
            form_path = form.path
            irs_form_id = int(form_file_name.replace('_public.xml', ''))
            print("form_file_name: ", form_file_name)
            tree = ET.parse(form_path)
            xml_data = tree.getroot()
            xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
            data_dict = dict(xmltodict.parse(xmlstr))
            return_version = data_dict['ns0:Return']['@returnVersion']

            try:
                return_data = data_dict['ns0:Return']['ns0:ReturnData']

                if 'ns0:IRS990EZ' in return_data.keys():
                    form_data = return_data['ns0:IRS990EZ']
                elif 'ns0:IRS990PF' in return_data.keys():
                    form_data = return_data['ns0:IRS990PF']
                elif 'ns0:IRS990' in return_data.keys():
                    form_data = return_data['ns0:IRS990']
                else:
                    raise Exception("Unhandled schema: " + return_version + "\n " + return_data.keys())

                if 'ns0:Organization501c' in form_data.keys():
                    org_data = form_data['ns0:Organization501c']
                    
                    if 'BusinessNameLine1' in org_data.keys():
                        entity_name = org_data['BusinessNameLine1']
                    elif 'ns0:Name' in org_data.keys():
                        entity_name = org_data['ns0:Name']['BusinessNameLine1']
                else:
                    raise Exception("Unhandled key set: " + form_data.keys())

                ein = org_data

                print("entity_name: ", entity_name)
                payload = {
                    "form_file_name": form_file_name,
                    "irs_form_id": irs_form_id,
                    "return_version": return_version,
                    "ein": ein,
                    "entity_name": entity_name
                }
                #store_form_to_db(payload)
            except Exception as err:
                traceback.print_tb(err.__traceback__)
                print("An error occurred")
                print("Debug info: return_version = ", return_version)
                print('data_dict return data keys:')
                print(data_dict['ns0:Return']['ns0:ReturnData'].keys())
                print('data_dict: ')
                print(data_dict)
                dom = xml.dom.minidom.parseString(xmlstr)
                pretty_xml_as_string = dom.toprettyxml()
                print(pretty_xml_as_string)
            finally:
                print("===")

main()
