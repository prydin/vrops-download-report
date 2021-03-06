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
  --token <API token (vR Ops Cloud only)>
  --report <report name> 
  --output <output file> 
  --format <pdf or csv>
```
Username+password and token are mutually exclusive. All arguments are required

## Example
On prem:
```
python dlreport.py --url http://myvrops.example.com --user admin --password topsecret --report "Capacity Report - Datastores" --format csv --output out.csv
```

Cloud:
```
python dlreport.py --url http://myvrops.example.com --token ABCDEF1234 --report "Capacity Report - Datastores" --format csv --output out.csv
```
