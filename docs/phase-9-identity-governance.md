# Phase 9 - Identity Governance

## Overview
Access reviews, entitlement management, terms of use, and identity secure score
baseline - the recurring oversight layer that keeps the identity environment clean
over time.

## Access Reviews

### Review 1 - IT Admin Group (Quarterly)
| Setting | Value |
|---|---|
| Name | Wardenix-IT-Admin-Access-Review |
| Resource | IT Team group |
| Frequency | Quarterly |
| Duration | 14 days |
| Reviewer | YetundeDuze (admin) |
| Auto-apply results | Yes |
| If no response | Remove access |

### Review 2 - HR Team Group (Monthly)
| Setting | Value |
|---|---|
| Name | Wardenix-CFO-HR-Access-Review |
| Resource | HR Team group |
| Frequency | Monthly |
| Duration | 7 days |
| Reviewer | Mei Chen |
| Auto-apply results | Yes |
| If no response | Remove access |

Design decision: IT Admin review uses the admin account as reviewer (privileged
access requires admin oversight). HR review uses Mei Chen as reviewer (peer
review, not self-review) - matches the original design requirement.

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

## Terms of Use

Name: Wardenix IT Admin Terms of Use
Content: 5-point acceptable use policy for privileged access activation
Status: Created and available for assignment

Licence boundary: Attaching Terms of Use to access packages requires the
Entra ID Governance licence (above P2). Terms of Use is created and confirmed
working - attachment to the access package is documented as a design decision
pending licence upgrade.

## Identity Secure Score

Baseline captured: 8/18/2026
Score at baseline: visible in docs/screenshots/phase-9-identity-secure-score-baseline.png
Tracking: score to be compared at each phase boundary as hardening improves posture

## Licence boundaries documented

| Feature | Requires | Status |
|---|---|---|
| Terms of Use on access packages | Entra ID Governance | Created, attachment blocked by licence |
| Lifecycle Workflows (Joiner/Mover/Leaver) | Entra ID Governance | Designed, not implemented |
| Entra ID roles as access package resources | Entra ID Governance | Documented, workaround used |

## Evidence
- docs/screenshots/phase-9-access-review-created.png
- docs/screenshots/phase-9-hr-access-review-created.png
- docs/screenshots/phase-9-access-package-created.png
- docs/screenshots/phase-9-terms-of-use-created.png
- docs/screenshots/phase-9-identity-secure-score-baseline.png
