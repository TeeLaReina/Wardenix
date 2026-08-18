"""
Wardenix - Phase 10: Wazuh to Azure Log Analytics forwarder (file-based)
Reads Wazuh alerts directly from alerts.json and forwards to Log Analytics.
"""
import json
import hashlib
import hmac
import base64
import datetime
import os
import requests

WARDENIX_WORKSPACE_ID = os.environ.get("WARDENIX_WORKSPACE_ID")
WARDENIX_WORKSPACE_KEY = os.environ.get("WARDENIX_WORKSPACE_KEY")
LOG_TYPE = "WazuhAlerts"
ALERTS_FILE = "/var/ossec/logs/alerts/alerts.json"

def build_signature(workspace_id, key, date, content_length, method, content_type, resource):
    x_headers = f"x-ms-date:{date}"
    string_to_hash = f"{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}"
    bytes_to_hash = string_to_hash.encode("utf-8")
    decoded_key = base64.b64decode(key)
    encoded_hash = base64.b64encode(
        hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
    ).decode("utf-8")
    return f"SharedKey {workspace_id}:{encoded_hash}"

def post_to_sentinel(data):
    body = json.dumps(data)
    method = "POST"
    content_type = "application/json"
    resource = "/api/logs"
    rfc1123date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_length = len(body)
    signature = build_signature(
        WARDENIX_WORKSPACE_ID, WARDENIX_WORKSPACE_KEY, rfc1123date,
        content_length, method, content_type, resource
    )
    uri = f"https://{WARDENIX_WORKSPACE_ID}.ods.opinsights.azure.com{resource}?api-version=2016-04-01"
    headers = {
        "Content-Type": content_type,
        "Authorization": signature,
        "Log-Type": LOG_TYPE,
        "x-ms-date": rfc1123date
    }
    r = requests.post(uri, data=body, headers=headers)
    return r.status_code

def read_last_alerts(n=50):
    alerts = []
    try:
        with open(ALERTS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        alerts.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return alerts[-n:]
    except Exception as e:
        print(f"Error reading alerts: {e}")
        return []

if __name__ == "__main__":
    print(f"Wardenix Wazuh→Sentinel forwarder v2 - {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    alerts = read_last_alerts(50)
    print(f"Read {len(alerts)} alerts from {ALERTS_FILE}")
    if alerts:
        status = post_to_sentinel(alerts)
        print(f"Posted to Log Analytics - HTTP {status}")
        if status == 200:
            print("Success - alerts forwarded to wardenix-sentinel")
        else:
            print(f"Warning - unexpected status code {status}")
    else:
        print("No alerts found")
