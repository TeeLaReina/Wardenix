"""
Wardenix - Phase 7: PIM Role Assignment Query Script
Queries Microsoft Graph API for PIM eligible assignments and activation history.
Requires: pip install msal requests
"""

import requests
import msal
import json
from datetime import datetime

# App registration credentials - load from environment variables in production
import os
TENANT_ID = os.environ.get("WARDENIX_TENANT_ID")
CLIENT_ID = os.environ.get("WARDENIX_CLIENT_ID")
CLIENT_SECRET = os.environ.get("WARDENIX_CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]


def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in result:
        raise Exception(f"Token acquisition failed: {result.get('error_description')}")
    return result["access_token"]


def get_eligible_assignments(token):
    """Get all PIM eligible role assignments in the tenant."""
    url = "https://graph.microsoft.com/v1.0/roleManagement/directory/roleEligibilitySchedules"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])


def get_activation_history(token):
    """Get PIM role activation requests from the last 7 days."""
    url = (
        "https://graph.microsoft.com/v1.0/roleManagement/directory/"
        "roleAssignmentScheduleRequests"
        "?$filter=requestType eq 'SelfActivate'"
        "&$expand=principal,roleDefinition"
        "&$orderby=createdDateTime desc"
    )
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])


def print_eligible_assignments(assignments):
    print("\n=== PIM Eligible Role Assignments ===")
    for a in assignments:
        principal = a.get("principalId", "unknown")
        role = a.get("roleDefinitionId", "unknown")
        status = a.get("status", "unknown")
        print(f"  Principal: {principal} | Role: {role} | Status: {status}")


def print_activation_history(activations):
    print("\n=== PIM Activation History (Self-Activate) ===")
    for a in activations:
        created = a.get("createdDateTime", "unknown")
        status = a.get("status", "unknown")
        principal = a.get("principal", {}).get("displayName", "unknown")
        role = a.get("roleDefinition", {}).get("displayName", "unknown")
        justification = a.get("justification", "none provided")
        print(f"  [{created}] {principal} activated {role} | Status: {status}")
        print(f"    Justification: {justification}")


if __name__ == "__main__":
    print(f"Wardenix PIM Query - {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    token = get_token()
    assignments = get_eligible_assignments(token)
    print_eligible_assignments(assignments)
    activations = get_activation_history(token)
    print_activation_history(activations)
