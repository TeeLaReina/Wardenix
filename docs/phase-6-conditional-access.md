# Phase 6 - Conditional Access Engineering

## Overview
Created six Conditional Access policies replacing Security Defaults for the 6 P2-licensed
accounts. The free-tier 20 users remain under Security Defaults with all policies validated
in Report-only mode via the What If tool before enabling.

## Policies

| Policy | Targets | Condition | Grant control |
|---|---|---|---|
| CA-01 - Require MFA for IT Admins | Wale Ibrahim, Mei Chen | All resources | Require MFA |
| CA-02 - Require MFA for Privileged Users | David Okafor, Sofia Larsen, Ama Mensah | All resources | Require MFA |
| CA-03 - Block Legacy Authentication | All 6 P2 users | Other clients + Exchange ActiveSync | Block access |
| CA-04 - Require MFA for All Cloud Apps | All 6 P2 users | All resources | Require MFA |
| CA-05 - Require MFA on Risky Sign-ins | All 6 P2 users | Sign-in risk: High + Medium | Require MFA |
| CA-06 - Require Entra Joined Device for IT Admins | Wale Ibrahim, Mei Chen | All resources | Require Entra joined device |

## Design decisions
- BreakGlass Admin was excluded from every policy - emergency recovery path preserved
- All policies were validated in Report-only mode via What If tool before enabling
- CA-03 scoped to legacy auth protocols only (Other clients + Exchange ActiveSync) - modern auth unaffected
- CA-05 requires P2 Identity Protection sign-in risk signal
- CA-06 enforces device trust - only DESKTOP-K8PDBGH (Entra joined in Phase 2) satisfies the control for IT admins
- Security Defaults disabled before CA policies enabled - the two cannot coexist

## What If validation
Validated against Azure Resource Manager app (ID: 797f4846-ba00-4fd7-ba43-dac1f8f63013),
Windows device platform, Mobile apps and desktop clients. CA-01 confirmed applying
Require MFA for Wale Ibrahim. CA-03 confirmed not applying for modern auth (correct -
only fires on Other clients).

Additional finding during validation: CA-06 blocked sign-in from SOC PC (black-orchid,
non-Entra-joined device) with error AADSTS9001011. CA-06 set to Report-only for
Phase 7 PIM testing window, re-enabled after.

## KQL queries - Log Analytics

### CA policy evaluation status
```kql
AADNonInteractiveUserSignInLogs
| summarize Count = count() by ConditionalAccessStatus
| order by Count desc
```
Result: All sign-ins ConditionalAccessStatus = notApplied - SOC PC not Entra-joined,
CA-06 device check fires before MFA grant control is evaluated.

### MFA enforcement rate
```kql
AADNonInteractiveUserSignInLogs
| summarize Count = count() by AuthenticationRequirement
| order by Count desc
```
Result: 54% singleFactorAuthentication, 46% multiFactor Authentication.
Ratio shifted after PIM activation (Wale completing MFA as part of role activation).

### CA policy details per sign-in
```kql
AADNonInteractiveUserSignInLogs
| where isnotempty(ConditionalAccessPolicies)
| project TimeGenerated, AccountUpn, ConditionalAccessPolicies, ConditionalAccessStatus, AuthenticationRequirement
| order by TimeGenerated desc
| limit 5
```
Result: CA-01 visible in ConditionalAccessPolicies field confirming policy evaluation
pipeline is working.

## Grafana dashboard - Wardenix Security Operations
URL: https://daintygerbil2221.grafana.net/d/ye2zlrr/wardenix-security-operations

Data source: Azure Monitor (App Registration - wardenix-grafana)
Connected to: wardenix-sentinel Log Analytics workspace

Entra ID diagnostic setting `wardenix-entra-to-sentinel` streams to wardenix-sentinel:
- SignInLogs
- NonInteractiveUserSignInLogs
- AuditLogs
- RiskyUsers
- UserRiskEvents

### Panels

| Panel | Table | Visualization | Finding |
|---|---|---|---|
| MFA Enforcement Rate | AADNonInteractiveUserSignInLogs | Pie chart | 54% MFA / 46% single-factor |
| CA Policy Status Distribution | AADNonInteractiveUserSignInLogs | Bar gauge | All notApplied - CA-06 device gap |
| PIM Role Activations | AuditLogs (RoleManagement) | Table | Wale Ibrahim activation confirmed 2026-08-18 18:03:27 |
| Identity Risk Events | AADUserRiskEvents / AADRiskyUsers | Table | Populated by future risk events |

## Evidence
- docs/screenshots/phase-6-ca-policies-all-enabled.png
- docs/screenshots/phase-6-kql-ca-policies-firing.png
- docs/screenshots/phase-6-kql-mfa-enforcement-rate.png
- docs/screenshots/phase-6-grafana-azure-monitor-connected.png
- docs/screenshots/phase-6-grafana-dashboard-full.png
- docs/screenshots/phase-6-grafana-mfa-panel.png
- docs/screenshots/phase-6-grafana-ca-status-panel.png
- docs/screenshots/phase-6-grafana-pim-panel.png
