# Phase 7 - Privileged Identity Management

## Overview
I gave just-in-time privileged access to the two IT Admin accounts. No standing admin
privileges meaning roles must be explicitly activated, MFA-verified, justified, and
approved before becoming active. Roles auto-expire after 1 hour.

## Eligible assignments

| User | Role | Assignment type | Approver |
|---|---|---|---|
| Wale Ibrahim | Identity Governance Administrator | Permanent eligible | Mei Chen |
| Mei Chen | Cloud Device Administrator | Permanent eligible | Wale Ibrahim |

## Role settings (both roles)
- Activation maximum duration: 1 hour
- On activation, require: Azure MFA
- Require justification on activation: Yes
- Require approval to activate: Yes

## Activation workflow - validated
1. Wale requested activation of Identity Governance Administrator with justification
2. Mei received approval request, reviewed justification, added her own justification, approved
3. Wale's role moved to Active assignments - state: Activated, end time: 1 hour from activation
4. Role will auto-expire - no manual deactivation required

## Additional finding - CA-06 device enforcement confirmed
Signing in as Wale from a non-Entra-joined device (SOC PC / black-orchid) triggered
AADSTS9001011: device policy contains unsupported required device state: domain_joined.
CA-06 blocked the sign-in as designed. CA-06 was then set to Report-only for PIM testing
and will be re-enabled after Phase 7 commit.

## Evidence
- docs/screenshots/phase-7-pim-eligible-assignments.png
- docs/screenshots/phase-7-pim-approval-request-mei.png
- docs/screenshots/phase-7-pim-wale-role-activated.png
- docs/screenshots/phase-7-ca06-device-policy-blocking-non-joined-device.png
