import requests
import json
import os
import sys
import time
import logging


log_month = time.strftime("%Y%m")
logdir = r'C:\Users\sk185610\OneDrive - NCR Corporation\Data\Project\NICS Automation\Import_integration'
logfile = logdir + '_log.' + log_month
logging.basicConfig(filename=logfile,format="%(asctime)-15s [%(levelname)s]: %(message)s",level=logging.DEBUG)

url = "https://idcs-90c20f8840524966a07f4f4901d2f65f.identity.oraclecloud.com/oauth2/v1/token"
payload='grant_type=password&username=yk185029&password=Balboa59*&scope=https%3A%2F%2FF24A70E30A0F4A54BBF640FC5CFE5365.integration.ocp.oraclecloud.com%3A443urn%3Aopc%3Aresource%3Aconsumer%3A%3Aall'
headers = {
'Authorization': 'Basic MmU5YjliM2Q2ZjMzNGQzNWExZWQwMGE1NDg4YmJhYjM6ZTU4N2U2N2QtNTg2Yi00NTNhLTlmZmItYzQ5NzIzYThlYTAy',
'Content-Type': 'application/x-www-form-urlencoded'
}


def connection_with_api(url, payload, header):
    try:
        response = requests.post(url, payload, headers=header)
        print ('Response status : ' + str(response.status_code))
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6

connection_with_api(url, payload, headers)

iar = input ("Enter the iar filename: ")
file = str(iar)

response = requests.request("POST", url, headers=headers, data=payload)

token = response.text
dict1= json.loads(token)
values_view = dict1.values()
value_iterator = iter(values_view)
token_value = next(value_iterator)

headers = {
        'authorization': "Bearer " + token_value,
        'Accept': 'application/json',
}


files = {
    'file': (file, open(file, 'rb')),
    'type': (None, 'application/octet-stream'),
}

env_url = 'https://nicdevelopment-ncrmiddlewarecs-ia.integration.ocp.oraclecloud.com'
file_name = 'DEMO_CHECK%7C01.00.0001'
response = requests.post( env_url +'/ic/api/integration/v1/integrations/archive', headers=headers, files=files)

if response.status_code == 204:
        print('Fresh deployment : ' + str(response.status_code))

        headers = {
        'authorization': "Bearer " + token_value,
        'Content-Type': 'application/json',
        'X-HTTP-Method-Override': 'PATCH',
        }

        data = open('update.json')
        response = requests.post( env_url + '/ic/api/integration/v1/integrations/' + file_name , headers=headers, data=data)
        print('Activating the intergration, the response is : ' + str(response.status_code))



elif response.status_code == 409:  #INTERGRATION ALREADY EXIST
        print('Integration already exist : ' + 'Response code : ' + str(response.status_code))

        headers = {
        'authorization': "Bearer " + token_value,
        'Accept': 'application/json',
        }

        response = requests.get( env_url + '/ic/api/integration/v1/integrations/' + file_name + '/activationStatus', headers=headers)

        token = response.text
        dict1= json.loads(token)
        values_view = dict1.values()
        value_iterator = iter(values_view)
        Status = next(value_iterator)
        print('Checking existing intergration Status')

        if Status == 'CONFIGURED':
                headers = {
                'authorization': "Bearer " + token_value,
                'Content-Type': 'application/json',
                'X-HTTP-Method-Override': 'PATCH',
                }

                data = open('update.json')
                response = requests.post( env_url + '/ic/api/integration/v1/integrations/' + file_name, headers=headers, data=data)

                print('Deploying and activating the new intergration' + ' and response : ' + str(response.status_code))


        elif Status == 'ACTIVATED':  #Incase integration already exist and is active, then deactivate it and active the new one
                headers = {
                'authorization': "Bearer " + token_value,
                'Content-Type': 'application/json',
                'X-HTTP-Method-Override': 'PATCH',
                }

                data = open('deactivate.json')
                response = requests.post( env_url + '/ic/api/integration/v1/integrations/' + file_name, headers=headers, data=data)
                print('status value is : ' + Status + "\n"  + 'Deactivating previous intergration')


                data = open('activate.json')  #After deactivating the existing intergration deploying/activating the new one
                response = requests.post( env_url + '/ic/api/integration/v1/integrations/' + file_name, headers=headers, data=data)
                print('Deploying and activating the new intergration' + ' and response : ' + str(response.status_code))

elif response.status_code == 400:
        print('File upload failure : No file is uploaded' + 'Response : ' + str(response.status_code))

elif response.status_code == 500:
        print('Server error' + 'Response : ' + str(response.status_code))

else:
        print('Response code : ' +  str(response.status_code) + 'Check Parameters : URL headers data are correctly passed or There exist any other error' )