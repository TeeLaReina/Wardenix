# Phase 1 - Identity Engineering

## Overview
26-user simulated organization provisioned entirely via Microsoft Graph API -
no manual portal clicks. 11 dynamic groups created and validated. Gitleaks
CI gate added to prevent credential leaks from the repo.

## Users provisioned (26)
Spread across departments: IT Admins (2), Executives (3), HR (1), Finance,
Marketing, Sales, Procurement, Engineering, Legal, Operations, Contractors.
Licensing split: 6 P2 accounts (IT Admins, Executives, HR Lead, BreakGlass),
20 Free tier accounts.

## Dynamic groups (11)
Created via Graph API with dynamic membership rules - e.g. IT Team
(`jobTitle -eq "IT Administrator"`), Executives, HR, Finance, etc.
No manual group membership management required.

## Gitleaks CI gate
GitHub Actions workflow added - blocks commits containing secrets, API keys,
or credentials. Runs on every push to main.

## Scripts
- `identity/provision_users.py` - creates all 26 users via Graph API
- `identity/create_groups.py` - creates 11 dynamic groups via Graph API

## Evidence
- docs/screenshots/phase-1-users-provisioned.png
