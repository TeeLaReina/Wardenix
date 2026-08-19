# Phase 10 - Log Pipeline & Multi-Engine Analysis

## Overview
Three detection engines - Entra ID (cloud identity), Wazuh (endpoint + network),
and Suricata (network IDS) - unified into a single queryable Log Analytics
workspace. All sources confirmed flowing and queryable via KQL and Grafana.

## Infrastructure

| Component | Value |
|---|---|
| Log Analytics workspace | wardenix-sentinel |
| Resource group | wardenix-rg |
| Region | East US |
| Azure subscription | Azure subscription 1 |
| Defender portal | Connected (Primary workspace) |
| Grafana Cloud | daintygerbil2221.grafana.net |
| Grafana data source | wardenix-grafana-azure-monitor-datasource |

## Data sources flowing into wardenix-sentinel

### 1. Entra ID - diagnostic settings
Configured via entra.microsoft.com → Monitoring & health → Diagnostic settings
Setting name: wardenix-entra-to-sentinel

| Log type | Table in Log Analytics |
|---|---|
| SignInLogs | SigninLogs |
| NonInteractiveUserSignInLogs | AADNonInteractiveUserSignInLogs |
| AuditLogs | AuditLogs |
| RiskyUsers | AADRiskyUsers |
| UserRiskEvents | AADUserRiskEvents |

### 2. Defender XDR connector (auto-configured)
Sentinel onboarded to Defender portal - Defender XDR connector automatically
configured. Includes Entra ID Protection alerts, Defender for Identity,
Defender for Endpoint, and Defender for Cloud Apps.

### 3. Wazuh → Log Analytics (file-based forwarder)
Script: infra/wazuh_to_sentinel.py
Method: Reads /var/ossec/logs/alerts/alerts.json, posts to Log Analytics
via HTTP Data Collector API
Schedule: Cron job every 15 minutes (/etc/cron.d/wazuh-sentinel)
Credentials: Stored in /etc/wazuh-sentinel.env (chmod 600)
Table: WazuhAlerts_CL
First successful run: 2026-08-18 22:50 UTC - 50 alerts, HTTP 200

## Grafana Cloud dashboard - Wardenix Security Operations

Data source: Azure Monitor (App Registration auth, wardenix-grafana)
URL: https://daintygerbil2221.grafana.net/d/ye2zlrr/wardenix-security-operations

### Panels

| Panel | Table | Finding |
|---|---|---|
| MFA Enforcement Rate | AADNonInteractiveUserSignInLogs | 54% MFA / 46% single-factor |
| CA Policy Distribution | AADNonInteractiveUserSignInLogs | All notApplied — CA-06 device gap |
| Risky Events | AADUserRiskEvents | 12 risk events from Tor simulation |
| PIM Role Activations | AuditLogs (RoleManagement) | Wale Ibrahim activation confirmed |
| Impossible Travel | AADNonInteractiveUserSignInLogs | Multi-country sign-ins detected |
| PIM Activation Anomalies | AuditLogs | Full PIM lifecycle visible |
| Mass Consent Grants | AuditLogs | 2 consent events — wardenix-grafana and wardenix-provisioning |
| Wazuh Alerts — Endpoint & Network Detection | WazuhAlerts_CL | SSH brute force (5710), memory pressure (5108) |

## KQL detection queries

See: detections/phase-10-log-pipeline-kql-queries.md

### Impossible travel detection
```kql
AADNonInteractiveUserSignInLogs
| where TimeGenerated > ago(7d)
| extend City = tostring(parse_json(LocationDetails).city)
| extend Country = tostring(parse_json(LocationDetails).countryOrRegion)
| summarize Cities = dcount(City), Countries = dcount(Country) by UserPrincipalName
| where Countries > 1
| order by Countries desc
```

### PIM activation anomalies
```kql
AuditLogs
| where TimeGenerated > ago(7d)
| where Category == "RoleManagement"
| where OperationName has "PIM"
| project TimeGenerated, OperationName, InitiatedBy, TargetResources, Result
| order by TimeGenerated desc
```

### Wazuh alerts by rule level
```kql
WazuhAlerts_CL
| project TimeGenerated, agent_name_s, rule_description_s, rule_level_d, rule_id_s
| order by TimeGenerated desc
```

### Mass consent grants
```kql
AuditLogs
| where TimeGenerated > ago(7d)
| where OperationName == "Consent to application"
| project TimeGenerated, InitiatedBy, TargetResources, Result
| order by TimeGenerated desc
```

## Wazuh infrastructure notes

- Wazuh indexer OOM-killed 2026-07-25 (heap 1024m on 3.8GB droplet)
- Fixed: heap reduced to 512m, 2GB swap added
- Wazuh API password reset via werkzeug scrypt hash in rbac.db
- DESKTOP-K8PDBGH (Wale's endpoint) showing disconnected - powered off since Phase 4
- Wazuh forwarder bypasses indexer - reads alerts.json directly

## Architectural note
Sentinel was deployed after the Phase 8 Tor browser attack simulation. The risky
sign-in detections are in Entra ID Protection (Phase 8 evidence) but predate
Sentinel deployment. Future risk events will appear in AADUserRiskEvents
automatically via the diagnostic settings pipeline.

## Evidence
- docs/screenshots/phase-10-sentinel-deployed.png
- docs/screenshots/phase-10-kql-signin-pipeline-volume.png
- docs/screenshots/phase-10-kql-impossible-travel.png
- docs/screenshots/phase-10-kql-pim-activation-anomalies.png
- docs/screenshots/phase-10-kql-stale-access.png
- docs/screenshots/phase-10-kql-consent-grants.png
- docs/screenshots/phase-10-wazuh-sentinel-forwarder-output.png
- docs/screenshots/phase-10-grafana-wazuh-alerts-panel.png
- docs/screenshots/phase-10-grafana-dashboard-full.png
