import requests
import json
import urllib3
import os
import argparse
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VRopsClient:
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url_base = ""

    token = ""

    def __init__(self, url_base, username=None, password=None, token=None):
        if token:
            # vR Ops cloud login
            self.url_base = url_base + '/suite-api/api'
            credentials = 'refresh_token=' + token
            result = requests.post(url='https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize',
                                   headers={ 'Content-Type': 'application/x-www-form-urlencoded' },
                                   data=credentials,
                                   verify=False)
            if result.status_code != 200:
                print(str(result.status_code) + " " + str(result.content))
                exit(1)
            json_data = json.loads(result.content)
            token = json_data["access_token"]
            self.headers["Authorization"] = "CSPToken " + token
        else:
            # On-prem login
            self.url_base = url_base + "/suite-api/api"
            credentials = json.dumps({"username": username, "password": password})
            result = requests.post(url=self.url_base + "/auth/token/acquire",
                                   data=credentials,
                                   verify=False, headers=self.headers)
            if result.status_code != 200:
                print(str(result.status_code) + " " + str(result.content))
                exit(1)
            json_data = json.loads(result.content)
            token = json_data["token"]
            self.headers["Authorization"] = "vRealizeOpsToken " + token

    def get(self, url):
        return requests.get(url=self.url_base + url,
                              headers=self.headers,
                              verify=False)
        return result


# Main program
#
parser = argparse.ArgumentParser(description='dlreport');
parser.add_argument('--url', help='The vR Ops URL', required=True)
parser.add_argument('--user', type=str, help='The vR Op suser', required=False)
parser.add_argument('--password', help='The vR Ops password', required=False)
parser.add_argument('--token', help='The vR Ops API Token (cloud only)', required=False)
parser.add_argument('--report', help='Report name', required=True)
parser.add_argument('--output', help='Output file', required=True)
parser.add_argument('--format', help='Output format (pdf or csv)', required=True)
args = parser.parse_args()

report_name = args.report
if args.user and args.password and not args.token:
    vrops = VRopsClient(args.url, username=args.user, password=args.password)
elif args.token:
    vrops = VRopsClient(args.url, token=args.token)
else:
    print("Either user/password or token must be specified")
    os.exit(1)

reports = vrops.get('/reports?status=COMPLETED&name=' + report_name).json()["reports"]
if len(reports) == 0:
    print("Report not found")
    os.exit(1)

# Convert dates to a sortable format and sort them
for report in reports:
    report['completionTime'] = datetime.strptime(report['completionTime'], '%a %b %d %H:%M:%S %Z %Y')
reports.sort(key=lambda r: r['completionTime'], reverse=True)
report_id = reports[0]["id"]

# Download the report
report_data =vrops.get('/reports/%s/download?format=%s' % (report_id, args.format))

# ...and dump it to file
f = open(args.output, "wb")
with f:
    f.write(report_data.content)