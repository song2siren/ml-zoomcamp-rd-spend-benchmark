"""Send an example request to the running web service.

Usage:
    uv run python test_predict.py                              # local service on port 9696
    uv run python test_predict.py https://<your-app>.fly.dev   # deployed service
"""
import json
import sys
import urllib.request

BASE_URL = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:9696'
URL = BASE_URL + '/predict'

company = {
    'net_sales': 250.0,
    'employees': 1200,
    'capex': 15.0,
    'operating_profit': 20.0,
    'year': 2024,
    'year_incorporated': 1998,
    'sector': 'Software & Computer Services',
    'country': 'UK',
    'reported_rnd': 30.0,
}

request = urllib.request.Request(
    URL,
    data=json.dumps(company).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
)
with urllib.request.urlopen(request) as response:
    print(json.dumps(json.load(response), indent=2, ensure_ascii=False))
