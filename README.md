# non-profit-browser
Non-profit organization informational tool.

## Description
The Internal Revenue Service (IRS) publishes a data set each year describing high-level aspects of charitable and non-profit organizations. This data contains information about assets and other financial data.

This project's goal is to make that data set more approachable through visualization and historical trend analysis.

## Feature Roadmap
Count the number of 501(c)(3) entities that have filed a Form 990 with the United States government. Spoiler alert: there are so many, they are crashing my instance trying to display them within a folder, even though I halted the download of the S3 bucket mid-2011. 

### Code Snippets

#### Download 990 XML Data
```AWS Command Line Interface
aws s3 cp s3://irs-form-990/index ./data/990/ --recursive
```
