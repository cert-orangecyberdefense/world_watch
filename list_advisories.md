# List Advisories

This is the expected result from using `/api/advisory/` endpoint with `limit: 2`.

The `count` indicated the total amount of possible results.

Performing a basic **HTTP** request:

```sh
curl -X 'GET' \
  'https://api-ww.cert.orangecyberdefense.com/api/advisory/?limit=2&offset=0' \
  -H 'accept: application/json' \
  -H 'Authorization: <TOKEN>'
```

An example of this request is present in the provided [`api_usage_example.py`](api_usage_example.py) file

The response should be:

```json
{
  "count": 1079,
  "items": [
    {
      "id": 1455,
      "tdc_id": 540692,
      "title": "Welcome to World Watch!",
      "severity": 0,
      "categories": [
        "other"
      ],
      "tags": [],
      "timestamp_created": "2000-12-31T00:00:00Z",
      "timestamp_updated": "2030-12-31T00:00:00Z",
      "license_agreement": "This advisory has been prepared and is the property of Orange Cyberdefense. Please don't redistribute this content without our agreement."
    },
    {
      "id": 1636,
      "tdc_id": 858347,
      "title": "Updated - Growing adoption of artificial intelligence by malicious actors",
      "severity": 1,
      "categories": [
        "ecosystem",
        "technique",
        "threat"
      ],
      "tags": [
        "ai",
        "takedown"
      ],
      "timestamp_created": "2024-02-19T11:40:09Z",
      "timestamp_updated": "2025-07-03T10:18:26Z",
      "license_agreement": "This advisory has been prepared and is the property of Orange Cyberdefense. Please don't redistribute this content without our agreement."
    }
  ]
}
```