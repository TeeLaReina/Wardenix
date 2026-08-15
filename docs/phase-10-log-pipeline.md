# Phase 10 - Log Pipeline & Multi-Engine Analysis

## Overview
Microsoft Sentinel was deployed on Azure Log Analytics workspace, connected to the
Defender portal (Unified SecOps Platform), with Entra ID sign-in telemetry
confirmed flowing and queryable via KQL.

## Infrastructure

| Component | Value |
|---|---|
| Log Analytics workspace | wardenix-sentinel |
| Resource group | wardenix-rg |
| Region | East US |
| Azure subscription | Azure subscription 1 |
| Defender portal | Connected (Primary workspace) |

## Data connectors
Sentinel was onboarded directly to the Defender portal (Unified SecOps Platform).
Per Microsoft documentation, the Microsoft Defender XDR connector is automatically
configured on Defender portal onboarding - this includes Microsoft Entra ID
Protection alerts, Defender for Identity, Defender for Endpoint, and Defender for
Cloud Apps. No manual connector configuration was required.

## KQL queries validated

### Sign-in pipeline volume (last 24h)
```kql
EntraIdSignInEvents
| where Timestamp > ago(24h)
| summarize EventCount = count() by bin(Timestamp, 1h)
| order by Timestamp asc
```
Result: 479 sign-in events across 5 hourly buckets. Spike of 349 events at
23:00 UTC on 15 Aug 2026 - corresponding to Phase 6-9 identity engineering
build activity.

### Sign-in events by account
```kql
EntraIdSignInEvents
| where Timestamp > ago(24h)
| summarize SignInCount = count() by AccountUpn
| order by SignInCount desc
```
Result: YetundeDuze@Wardenix.onmicrosoft.com - 467 sign-ins confirmed in pipeline.

## Architectural note - Phase 8 attack simulation not in Sentinel pipeline
Sentinel was deployed after the Phase 8 Tor browser attack simulation. The risky
sign-in (Anonymous IP + Malicious IP detections, High severity) is confirmed in
Entra ID Protection (Phase 8 evidence) but predates Sentinel deployment and is
not in the Sentinel pipeline. In a production environment, Sentinel would be
pre-deployed and would have ingested these alerts automatically via the Defender
XDR connector. This is documented as a sequencing constraint, not a gap in the
detection architecture.

## Evidence
- docs/screenshots/phase-10-sentinel-deployed.png
- docs/screenshots/phase-10-kql-signin-pipeline-volume.png
