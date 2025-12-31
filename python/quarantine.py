import requests
import json

# Elasticsearch and mock API endpoints
ES_HOST = "http://localhost:9200"
INDEX = "email-phishing-*"
QUARANTINE_API = "http://localhost:5000/quarantine"

# Query for quarantined emails
query = {
    "query": {
        "match": {
            "verdict": "quarantined"
        }
    }
}

# Fetch quarantined emails
response = requests.get(f"{ES_HOST}/{INDEX}/_search", headers={"Content-Type": "application/json"}, data=json.dumps(query))
hits = response.json().get("hits", {}).get("hits", [])

print(f"Found {len(hits)} quarantined emails.")

# Send each to mock quarantine API
for hit in hits:
    email = hit["_source"]
    payload = {
        "sender": email.get("sender"),
        "recipient": email.get("recipient"),
        "subject": email.get("subject"),
        "urls": email.get("urls"),
        "attachments": email.get("attachments"),
        "timestamp": email.get("@timestamp")
    }
    r = requests.post(QUARANTINE_API, json=payload)
    print(f"Quarantined: {email.get('subject')} → Status: {r.status_code}")
