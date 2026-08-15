# Phase 8 - Identity Protection: Risk Detection and Investigation

## Overview
Simulated a real attack scenario using Tor Browser to trigger Identity Protection
risk detections, investigated the findings across all three ID Protection reports,
and remediated the affected user account.

## Risk detections generated

| Detection type | Risk level | User | IP address | Location |
|---|---|---|---|---|
| Anonymous IP address | High | Wale Ibrahim | 2001:67c:e60c:0c:192:42:116:45 | Amsterdam, NL |
| Malicious IP address | High | Wale Ibrahim | 2001:67c:e60c:0c:192:42:116:45 | Amsterdam, NL |

## What happened - full chain
1. Tor Browser used to simulate anonymous/malicious IP sign-in attempt as Wale Ibrahim
2. Microsoft threat intelligence identified the Tor exit node as both anonymous and malicious
3. Smart lockout triggered before password entry - account temporarily locked (error 50053)
4. Sign-in recorded in Risky sign-ins: Status Failure, resource Azure Resource Manager
5. Wale Ibrahim flagged in Risky users: At risk, High (1 of 26 users, 3.57%)
6. CA-05 (Require MFA on risky sign-ins) would have fired had the sign-in completed

## Remediation
- Confirmed user safe in ID Protection - risk state cleared
- Account lockout expired / sessions revoked
- Detections remain in audit log for historical record

## Key finding
Identity Protection detected and responded at the network layer before authentication
completed. The malicious IP detection came from Microsoft threat intelligence, not
just the anonymous IP heuristic - the Tor exit node was on an active blocklist.

## Evidence
- docs/screenshots/phase-8-risk-detections-tor.png
- docs/screenshots/phase-8-risky-sign-in-details-tor.png
- docs/screenshots/phase-8-risky-user-wale.png
- docs/screenshots/phase-8-wale-confirmed-safe.png
