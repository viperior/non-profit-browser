# Sample 3 Form 990s from each year and attempt pull sample data:
# Entity Name
# Description
# Location
# Tax Period Begin Date
# Gross Receipts

import datetime
import json
import random
import urllib.request as request

start_year = 2013
end_year = datetime.datetime.utcnow().year + 1
year_range = range(start_year, end_year)
index_file_prefix = 'https://s3.amazonaws.com/irs-form-990/index_'
samples_per_year = 3
sample_indices = {}
target_data_file_path = 'data/sample_990s.json'

# Generate random numbers to pull 990 data.
with open('data/yearly_filing_counts.json', 'r') as file:
    json_data = json.load(file)
    
    for year in json_data:
        current_year = year['Year']
        current_filing_count = year['Filing Count']
        current_sample_indices = []
        sample_counter = 0
        
        while sample_counter < 3:
            current_sample_indices.append(random.randrange(0, current_filing_count))
            sample_counter += 1
            
        sample_indices[current_year] = current_sample_indices

sample_filings = []

for year in range(start_year, end_year):
    with request.urlopen(index_file_prefix + str(year) + '.json') as response:
        source = response.read()
        json_data = json.loads(source)
        source = None
        
        for sample_index in sample_indices[year]:
            filing = json_data['Filings' + str(year)][sample_index]
            sample_filings.append(filing)
            print(filing)
            
with open(target_data_file_path, 'w') as file:
    json.dump(sample_filings, file)
