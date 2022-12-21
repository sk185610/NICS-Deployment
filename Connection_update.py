import requests
import json

url = 'https://xx.integration.ocp.oraclecloud.com/ic/api/integration/v1/connections/'
cred = ('myuser', 'mypassword')

response=requests.get(
  url,
  auth = cred
)

dict = response.json()

#converting dict to json 
data = json.dumps(dict)

index=len(dict['items'])

for i in range(index):
  if "ERP" in json.loads(data)['items'][i]['id']:
    finalurl=url+ json.loads(data)['items'][i]['id']
    resp=requests.post(finalurl,headers=h,auth=cred,data=payload)
    print(f"Updating the Password for Connection with ID: {json.loads(data)['items'][i]['id']}\n Result is: {resp}")

payload="{\"securityProperties\":[{\"propertyName\":\"password\",\"propertyValue\": \"<newpassword>\"}]}"
h = {'Content-type': 'application/json','Accept': 'application/json','X-HTTP-Method-Override': 'PATCH'}