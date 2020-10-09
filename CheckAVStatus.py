import os
import sys
import time
import requests

url_post = 'https://www.virustotal.com/vtapi/v2/file/scan'
url_result = 'https://www.virustotal.com/vtapi/v2/file/report'

api_key = os.environ['VIRUS_TOTAL_API_KEY']
post_params = {'apikey': api_key}
files = {'file': ('dist/A32NX_Downloader.exe', open('dist/A32NX_Downloader.exe', 'rb'))}
print('Requesting AV scan for new exe file!')
post_response = requests.post(url_post, files=files, params=post_params)
if post_response.status_code == 200:
    print('Scan started!')
    data = post_response.json()
    if data['response_code'] == 1:
        timeout = time.time() + 60 * 5
        while True:
            if time.time() > timeout:
                break
            time.sleep(30)
            try:
                result_params = {'apikey': api_key, 'resource': data['resource']}
                result_response = requests.get(url_result, params=result_params).json()
                print(f'Scan finished total positives {result_response["positives"]}')
                print(f'Scan URL {result_response["permalink"]}')
                if 2 >= result_response['positives']:
                    print('Accepted exe, within acceptable parameters')
                    sys.exit(0)
                elif result_response['positives'] > 2:
                    print('Denied exe, NOT within acceptable parameters! Please verify')
                    sys.exit(1)
            except KeyError:
                pass
print('Could not verify exe! Please run again or manually check the artefact.')
sys.exit(1)
