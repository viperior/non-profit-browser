# non-profit-browser
Non-profit organization informational tool

## Description
The Internal Revenue Service (IRS) publishes a data set each year describing high-level aspects of charitable and non-profit organizations. This data contains information about assets and other financial data.

This project's goal is to make that data set more approachable through visualization and historical trend analysis.

### Code Snippets

#### Download 990 XML Data
```AWS Command Line Interface
aws s3 cp s3://irs-form-990/index ./data/990/ --recursive
```
