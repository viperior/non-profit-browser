import pandas as pd
import plotly.express as px

df = pd.read_json(path_or_buf = 'data/yearly_filing_counts.json')
fig = px.bar(df, x = 'Year', y = 'Filing Count')
fig.write_html('sample/data/990/filing-count-per-year.html')
