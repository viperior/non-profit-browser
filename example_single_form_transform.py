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

def main():
    form_path = 'data/indices/201014493492009090_public.xml'
    tree = ET.parse(form_path)
    xml_data = tree.getroot()
    xml_str = ET.tostring(xml_data, encoding='utf-8', method='xml')
    return_filer_name = get_return_filer_name(xml_str)
    print('return_filer_name: ', return_filer_name)

main()
