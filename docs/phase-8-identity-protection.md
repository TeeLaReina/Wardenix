# Phase 8 - Identity Protection: Risk Detection and Investigation

## Overview
Configured risk-based Conditional Access, simulated real attack scenarios to generate
risk detections, investigated findings across all ID Protection reports, and
remediated affected accounts. Extended with CA-07 user risk policy requiring password
change on high-risk users.

## Conditional Access policies added

### CA-05 - Require MFA on Risky Sign-ins (Phase 6)
- Targets: All 6 P2 users (BreakGlass excluded)
- Condition: Sign-in risk High or Medium
- Grant: Require MFA
- Status: On

### CA-07 - Require Password Change on High User Risk
- Targets: Wale Ibrahim, Mei Chen, David Okafor, Sofia Larsen, Ama Mensah
- Condition: User risk High
- Grant: Require risk remediation (enforces MFA + secure password change)
- Status: On

## Attack simulation - Tor browser sign-in

Two Tor browser sessions run against wale.ibrahim@Wardenix.onmicrosoft.com:
- Session 1 (15 Aug 2026, pre-diagnostic settings): Anonymous IP + Malicious IP
  detected, High risk, account locked by smart lockout (error 50053)
- Session 2 (18 Aug 2026, post-diagnostic settings): 12 risk events captured in
  AADUserRiskEvents - anonymizedIPAddress detection type, mix of High and Medium
  risk levels, two Tor exit node IPs detected in real-time

## Risk detections generated (Session 2 - in Log Analytics pipeline)

| Timestamp | User | Detection type | Risk level | Risk state | IP |
|---|---|---|---|---|---|
| 2026-08-18 18:43:57 | Wale Ibrahim | anonymizedIPAddress | high | atRisk | 2a03:e600:100::3 |
| 2026-08-18 18:44:18–18:46:03 | Wale Ibrahim | anonymizedIPAddress | medium/high | remediated | 2a06:1700:3:19::1 |

## Investigation workflow

### Step 1 - Detect
- ID Protection → Risk detections: Two detection types fire simultaneously
  (Anonymous IP address + Malicious IP address) - Tor exit node on active blocklist
- ID Protection → Risky sign-ins: Sign-in recorded as Failure (error 50053)
  - smart lockout fired before password entry
- ID Protection → Risky users: Wale Ibrahim flagged At risk, High (3.57% of 26 users)

### Step 2 - Investigate
- Check sign-in details: Application = Azure Portal, Resource = Azure Resource Manager
- Verify IP reputation: 2a03:e600:100::3 and 2a06:1700:3:19::1 - known Tor exit nodes
- Check DetectionTimingType: realtime - Microsoft caught this as it happened
- Cross-reference with Wazuh: endpoint telemetry for DESKTOP-K8PDBGH during
  same window (no anomalous process activity - attack was cloud-only)

### Step 3 - Decision
- Determine: simulated attack (known Tor session) → confirm user safe
- If real attack: confirm user compromised → force password reset → revoke sessions
  → investigate lateral movement → check PIM activation history for privilege abuse

### Step 4 - Remediate
- Confirmed user safe in ID Protection → risk state cleared → remediated
- CA-07 would have enforced password change if risk had been genuine High user risk
- Account lockout cleared automatically after smart lockout window

## KQL queries

### Risk events with full columns
```kql
AADUserRiskEvents
| project TimeGenerated, UserDisplayName, RiskEventType, RiskLevel, RiskState, IpAddress, DetectionTimingType
| order by TimeGenerated desc
```

### High risk users currently at risk
```kql
AADRiskyUsers
| where RiskLevel == "high" and RiskState == "atRisk"
| project TimeGenerated, UserDisplayName, UserPrincipalName, RiskLevel, RiskState, RiskDetail
| order by TimeGenerated desc
```

### Risk events summary by type
```kql
AADUserRiskEvents
| summarize Count = count() by RiskEventType, RiskLevel
| order by Count desc
```

## Grafana dashboard - Wardenix Security Operations
Panel: Identity Risk Events
Table: AADUserRiskEvents
Query: risk events with TimeGenerated, UserDisplayName, RiskEventType, RiskLevel,
RiskState, IpAddress, DetectionTimingType
Finding: 12 risk events captured from Tor browser session 2 (18 Aug 2026)

## Evidence
- docs/screenshots/phase-8-risk-detections-tor.png
- docs/screenshots/phase-8-risky-sign-in-details-tor.png
- docs/screenshots/phase-8-risky-user-wale.png
- docs/screenshots/phase-8-wale-confirmed-safe.png
- docs/screenshots/phase-8-ca07-user-risk-policy.png
- docs/screenshots/phase-8-grafana-risk-events-panel.png
