import os
import return_filing
import xml.dom.minidom
import xml.etree.ElementTree as ET
import xmltodict

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
