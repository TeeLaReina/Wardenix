# Phase 9 - Identity Governance

## Overview
Access reviews and entitlement management configured to answer the core governance
question: who has access to what, and how do we know they still need it?

## Access Review

| Setting | Value |
|---|---|
| Name | Wardenix-IT-Admin-Access-Review |
| Resource | IT Team group |
| Frequency | Quarterly |
| Duration | 14 days |
| Reviewer | YetundeDuze (admin) |
| Auto-apply results | Yes |
| If no response | Remove access |

Quarterly recertification of IT Admin group membership. If the reviewer does not
act within 14 days, access is automatically removed. This closes the access creep
vector where accounts accumulate permissions that are never reviewed.

## Access Package

| Setting | Value |
|---|---|
| Name | IT Admin Access Package |
| Resource | wardenix-provisioning (enterprise app) |
| Resource role | Default Access |
| Who can request | Admin only (no self-service) |
| Approval required | Yes - YetundeDuze |
| Assignment expiry | 365 days |
| Access reviews | Quarterly, 14-day window, auto-apply |

## Licence boundary - documented architectural decision
Two capabilities were blocked by licence during this phase:

1. **Entra ID roles as access package resources** (e.g. Identity Governance
   Administrator) - requires Entra ID Governance licence (above P2). Workaround:
   used the wardenix-provisioning enterprise app as the resource instead.

2. **Lifecycle Workflows** - automate joiner/mover/leaver events (onboard new
   user → assign access package, offboard → revoke access, disable account).
   Requires Entra ID Governance licence. Architectural design documented below
   but not implemented in this phase.

## Lifecycle Workflows - architectural design (not implemented)

| Trigger | Workflow | Actions |
|---|---|---|
| User created (Joiner) | New IT Admin onboarding | Assign IT Admin Access Package, send welcome email |
| Department change (Mover) | Access update | Remove old access package, assign new one |
| User disabled (Leaver) | Offboarding | Revoke all access packages, disable account, notify admin |

## Evidence
- docs/screenshots/phase-9-access-review-created.png
- docs/screenshots/phase-9-access-package-created.png
