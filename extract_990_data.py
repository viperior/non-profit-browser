import json
import pandas as pd
import urllib
import xmltodict

with open('data/sample_990s.json', 'r') as file:
    json_data = json.load(file)
    
ignored_return_types = ['990PF']
ignored_return_versions = ['2011v1.5']
    
url_prefix = 'https://s3.amazonaws.com/irs-form-990/'
min_filing_year = 2013
max_filing_year = 2019
min_return_version_year = 2013
max_return_version_year = 2013

for current_return in json_data:
    current_url = current_return['URL']
    
    print(current_url)

    year_form_filed = int(current_url.replace(url_prefix, '')[:4])
    print('Year form filed: ' + str(year_form_filed))
    
    if year_form_filed < min_filing_year or year_form_filed > max_filing_year:
        print('Skipping because this return was filed too long ago...')
        continue

    file = urllib.request.urlopen(current_url)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    
    return_dict = {}
    
    return_dict['return_version'] = data['Return']['@returnVersion']
    print(return_dict['return_version'])
    
    return_version_year = int(return_dict['return_version'][:4])
    
    print(return_version_year)
    
    if return_version_year < min_return_version_year or return_version_year > max_return_version_year:
        print('Skipping because this return was for a tax year that was too long ago...')
        continue
    
    return_dict['tax_year'] = data['Return']['ReturnHeader']['TaxYr']
    print(return_dict['tax_year'])
    
    return_dict['return_type_code'] = data['Return']['ReturnHeader']['ReturnTypeCd']
    return_dict['ein'] = data['Return']['ReturnHeader']['Filer']['EIN']
    return_dict['org_name'] = data['Return']['ReturnHeader']['Filer']['BusinessName']['BusinessNameLine1']
    return_dict['street_address_line_1'] = data['Return']['ReturnHeader']['Filer']['USAddress']['AddressLine1']
    return_dict['street_address_line_2'] = data['Return']['ReturnHeader']['Filer']['USAddress']['AddressLine2']
    return_dict['city'] = data['Return']['ReturnHeader']['Filer']['USAddress']['City']
    return_dict['state'] = data['Return']['ReturnHeader']['Filer']['USAddress']['State']
    return_dict['zip_code'] = data['Return']['ReturnHeader']['Filer']['USAddress']['ZIPCode']
    
    print(data['Return']['ReturnData'].keys())
    print(return_dict)
