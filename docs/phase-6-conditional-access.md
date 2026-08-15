# Phase 6 - Conditional Access Engineering

## Overview
Six Conditional Access policies replacing Security Defaults for the 6 P2-licensed
accounts. Free-tier 20 users remain under Security Defaults.

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
- BreakGlass Admin excluded from every policy - emergency recovery path
- All policies validated in Report-only mode via What If tool before enabling
- CA-03 scoped to legacy auth protocols only - modern auth unaffected
- CA-05 requires P2 Identity Protection sign-in risk signal
- CA-06 enforces device trust - only DESKTOP-K8PDBGH (Entra joined, Phase 2) satisfies the control for IT admins

## Evidence
Screenshot: docs/screenshots/phase-6-ca-policies-all-enabled.png
