import datetime
import json
import urllib.request as request

first_year_of_available_filings = 2013
index_file_path_prefix = 'https://s3.amazonaws.com/irs-form-990/index_'

# Get the current year.
current_time = datetime.datetime.utcnow()
current_year = current_time.year

# Generate a range with the years of the 990 filings the IRS has made publicly available.
irs_990_filings_year_range = list(range(first_year_of_available_filings, current_year + 1))

# Generate a dictionary containing overall information about each filing year.
irs_990_filings = {}

for year in irs_990_filings_year_range:
    filing_dict = {}
    filing_dict['index_file_path'] = index_file_path_prefix + str(year) + '.json'
    irs_990_filings[year] = filing_dict

# Count the number of filings per year.
for filing_year in irs_990_filings_year_range:
    with request.urlopen(irs_990_filings[filing_year]['index_file_path']) as response:
        source = response.read()
        json_data = json.loads(source)
        source = None
        primary_node_key = 'Filings' + str(filing_year)
        current_filing_count = len(json_data[primary_node_key])
        irs_990_filings[filing_year]['filing_count'] = current_filing_count

# Display the counts.
for filing_year in irs_990_filings_year_range:
    print('Filing year: ' + str(filing_year))
    print('Count: ' + str(irs_990_filings[filing_year]['filing_count']))
