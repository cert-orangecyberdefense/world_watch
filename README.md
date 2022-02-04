World Watch API documentation provided to each client that was granted access to the REST API service, located at: api-tdc.cert.orangecyberdefense.com.


Authentication endpoint:

Located at: https://api-tdc.cert.orangecyberdefense.com/v1/auth/
Requires a API key pair of credentials generated from your profile on TDC portal personal account here: https://portal.cert.orangecyberdefense.com/admin/api.
If you subscribed to the API access but don't see this page, you need to contact your Orange Cyberdefense representative.

Restrict ouptut per service:

If you subscribed to our Cybercrime services on top of World Watch service, all advisories (i.e. JSON documents) are available from the main API endpoint:
https://api-tdc.cert.orangecyberdefense.com/v1/cybalerts/

You need to filter by specific 'offer_name' or 'service_name' to only list alerts/advisories related to a specific service. For World Watch, you can thus use for example: 'service_name' = 'World Watch'.

i.e.

====
params = ( ('limit', 'nbelment'),
('offset', 'index'),
('service_name', 'World Watch')
)
response = requests.get('https://api-tdc.cert.orangecyberdefense.com/v1/cybalerts/', headers=headers, params=params)

