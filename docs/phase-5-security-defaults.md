# Phase 5 — Baseline Protection: Security Defaults

## Status
Enabled (automatically by Microsoft at tenant creation — confirmed August 2026)

## What Security Defaults enforces
- All users must register for MFA (Microsoft Authenticator)
- Admins must complete MFA on every sign-in
- Users challenged for MFA on risk signals (new device, unusual location)
- Legacy authentication protocols blocked (IMAP, SMTP, POP3, older Office clients)
- Device code flow blocked

## Security Defaults vs. Conditional Access

Security Defaults is the free-tier all-or-nothing baseline. Conditional Access
(Phase 6) replaces it for P2-licensed accounts with granular per-user, per-app,
per-location, and risk-based policies that allow exceptions (e.g. break-glass),
enforce device compliance, and require P1/P2 licensing. Security Defaults remains
active for the free-tier 20 users who have no CA entitlement.

## Evidence
Screenshot: docs/screenshots/phase-5-security-defaults-enabled.png
