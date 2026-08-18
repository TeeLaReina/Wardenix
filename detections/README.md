# Detections

KQL queries, Sigma rules, and detection logic for the Wardenix security platform.

## Structure

| File | Phase | Description |
|---|---|---|
| phase-6-ca-kql-queries.md | 6 | Conditional Access sign-in log queries - CA policy evaluation, MFA enforcement rate |

## Data sources

| Source | Platform | Tables |
|---|---|---|
| Entra ID sign-in logs | Azure Log Analytics / Defender Advanced Hunting | SigninLogs, EntraIdSignInEvents |
| Entra ID audit logs | Azure Log Analytics | AuditLogs |
| Entra ID risk events | Azure Log Analytics | RiskyUsers, UserRiskEvents |
| Endpoint telemetry | Wazuh dashboard | wazuh-alerts-* |
| Network alerts | Suricata eve.json | eve.json |

## Query language
All Log Analytics queries use KQL (Kusto Query Language).
All Defender portal queries use KQL against the Advanced Hunting schema.
