# Phase 10 - Log Pipeline KQL Queries

## Impossible travel detection
```kql
AADNonInteractiveUserSignInLogs
| where TimeGenerated > ago(7d)
| extend City = tostring(parse_json(LocationDetails).city)
| extend Country = tostring(parse_json(LocationDetails).countryOrRegion)
| summarize Cities = dcount(City), Countries = dcount(Country) by UserPrincipalName
| where Countries > 1
| order by Countries desc
```
Evidence: docs/screenshots/phase-10-kql-impossible-travel.png

## PIM activation anomalies
```kql
AuditLogs
| where TimeGenerated > ago(7d)
| where Category == "RoleManagement"
| where OperationName has "PIM"
| project TimeGenerated, OperationName, InitiatedBy, TargetResources, Result
| order by TimeGenerated desc
```
Result: Full PIM activation lifecycle visible - requested, approved, completed, expired
Evidence: docs/screenshots/phase-10-kql-pim-activation-anomalies.png

## Stale access detection (accounts inactive >14 days)
```kql
AADNonInteractiveUserSignInLogs
| where TimeGenerated > ago(30d)
| summarize LastSignIn = max(TimeGenerated) by UserPrincipalName
| where LastSignIn < ago(14d)
| order by LastSignIn asc
```
Result: No results - all users active within 14 days (correct for active lab environment)
Evidence: docs/screenshots/phase-10-kql-stale-access.png

## Mass consent grants detection
```kql
AuditLogs
| where TimeGenerated > ago(7d)
| where OperationName == "Consent to application"
| project TimeGenerated, InitiatedBy, TargetResources, Result
| order by TimeGenerated desc
```
Result: 2 consent events - wardenix-grafana and wardenix-provisioning app registrations
Evidence: docs/screenshots/phase-10-kql-consent-grants.png

## Sign-in pipeline volume (baseline)
```kql
AADNonInteractiveUserSignInLogs
| where TimeGenerated > ago(24h)
| summarize EventCount = count() by bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```
Evidence: docs/screenshots/phase-10-kql-signin-pipeline-volume.png
