# vRealize Operations Report Downloader
A simple utility that dowloads a report from vRealize Operations. Currently, only the latest report is downloaded.

## Installing
```bash
git clone https://github.com/prydin/vrops-download-report
pip install --user -r requirements.txt
```

## Usage
```
python dlreport.py [-h] 
  --url <vR Ops URL> 
  --user <vR Ops User> 
  --password <vR Ops password> 
  --report <report name> 
  --output <output file> 
  --format <pdf or csv>
```
All arguments are required

## Example
```
python dlreport.py --url http://myvrops.example.com --user admin --password topsecret --report "Capacity Report - Datastores" --format csv --output out.csv
```
