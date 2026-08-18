# Phase 6 - Conditional Access KQL Queries

## CA policy evaluation status distribution
```kql
EntraIdSignInEvents
| where Timestamp > ago(7d)
| summarize Count = count() by ConditionalAccessStatus
```
Result: 765 sign-ins with ConditionalAccessStatus = 2 (policies not applied).
All sign-ins from admin account on non-Entra-joined device (black-orchid) -
CA-06 device compliance gap produces "not applied" status. CA policy names
visible in ConditionalAccessPolicies field confirming evaluation is occurring.

## MFA enforcement rate
```kql
EntraIdSignInEvents
| where Timestamp > ago(7d)
| summarize Count = count() by AuthenticationRequirement
```
Result: 755 sign-ins, all singleFactorAuthentication. Admin account exempt
from MFA enforcement because CA-06 device check fails first - policy
evaluation stops before MFA grant control is reached.

## CA policy details per sign-in
```kql
EntraIdSignInEvents
| where Timestamp > ago(7d)
| where isnotempty(ConditionalAccessPolicies)
| project Timestamp, AccountUpn, ConditionalAccessPolicies, ConditionalAccessStatus, AuthenticationRequirement
| order by Timestamp desc
| limit 5
```
Result: CA-01 (Require MFA for IT Admins) visible in ConditionalAccessPolicies
field against YetundeDuze sign-ins - confirms policy evaluation pipeline is
working and CA policy details are queryable in Log Analytics.
