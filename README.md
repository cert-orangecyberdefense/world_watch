World Watch API documentation provided to each client that was granted access to the REST API service, located at: api-tdc.cert.orangecyberdefense.com.

Authentication endpoint:

Located at: https://api-tdc.cert.orangecyberdefense.com/v1/auth/
Requires a API key pair of credentials generated from your profile on TDC portal personal account here: https://portal.cert.orangecyberdefense.com/admin/api.
If you subscribed to the API access but don't see this page, you need to contact your Orange Cyberdefense representative.



First, you need to obtain your token using your customer ID (sent by our support team) and a secret API key.

To get the secret API key credential:<br/>
• go to the TDC (https://cert.orangecyberdefense.com)<br/>
• log in using your administrator account<br/>
• click on Administration, then on the API tab<br/>
• your client identifier will be displayed<br/>
• click on the “generate API key” button to get your API key<br/>
• your API key will be displayed on the screen<br/>

Then, to authenticate against the TDC API, you need to send a REST POST request to the /v1/auth/ entrypoint.  The body of your request must be specified as being json content by setting the header “Content-Type” to “application/json”. In the body of your request, you must provide your username and password, being respectively the client identifier andthe API key that the TDC provided you in the API tab.

For example, in python 3, you can execute the following code to get your token.,

     
```

#!python 

from urllib import request
import requests
import json



#get token <br/>
query = request.Request('https://api-tdc.cert.orangecyberdefense.com/v1/auth/', method='POST',
data='{"username": "     your USERNAME      ", '
'"password": "     YOUR API KEY          "}'.encode('utf-8'),
headers={'Content-Type': 'application/json'},)
with request.urlopen(query) as response:content = json.loads(response.read().decode('utf-8'))
token = content['token']
```



Restrict output per service:

If you subscribed to our Cybercrime services on top of World Watch service, all advisories (i.e. JSON documents) are available from the main API endpoint:
https://api-tdc.cert.orangecyberdefense.com/v1/cybalerts/

For example, in Python 3, you can run the following code to get all the alerts.
```
nbelement = 20
index=1
file = open("file_result.json", "w")
file.write("")
file = open("file_result.json", "a", encoding='utf-8')

url ='https://api-tdc.cert.orangecyberdefense.com/v1/cybalerts/'
response = requests.get('https://api-tdc.cert.orangecyberdefense.com/v1/cybalerts/', headers=headers)
request=json.loads(response.content)
maxnumber = request['count']
modulo = maxnumber % nbelement

if (maxnumber != 0):
    while request['next'] is not None:
        url = str(request['next'])
        i=0
                       
        while i!=nbelement:
            file.write(str(request['results'][i]) + "\n")
            print(request['results'][i])  
            i=i+1
            
                            
        i=0
        response = requests.get(url, headers=headers)
        request=json.loads(response.content)

                                     
    if request['next'] is None :
        if (modulo == 0):                       
            modulo =nbelement               
        while i!=modulo:
            file.write(str(request['results'][i]) + "\n")
            print(request['results'][i])
            i=i+1
            
        i=0
		
```
 

There are many parameters available to filter your search more precisely, to use them, just add them when you run your query, for example to filter by 'offer_name' or 'service_name' specifically to list only alerts/advice related to a specific service. So for World Watch, you could use for example: 'service_name' = 'World Watch'.

i.e.

```
params = ( 
('service_name', 'World Watch'),
)

response = requests.get('https://api-tdc.cert.orangecyberdefense.com/v1/cybalerts/', headers=headers, params=params)
```


The list of the different parameters allowing to filter your searches are available from the setting_file




