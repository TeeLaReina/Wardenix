# Phase 4 - Attack, Risk Assessment & Hardening

## Overview
Attacked the unhardened endpoint, formally risk-registered every finding,
hardened based on findings, re-tested to measure genuine risk reduction.
Attack before harden - always.

## Pre-attack baseline
- Static IPs: kalip (attacker) = 10.10.10.10, endpoint (target) = 10.10.10.20
- PRE-ATTACK-BASELINE snapshots taken on both VMs
- Isolation re-verified: clipboard, shared folders, drag-and-drop disabled

## Attack sequence
- Payload: windows/meterpreter/reverse_tcp, LHOST 10.10.10.10, LPORT 4444
- Delivered via python3 -m http.server 8080, downloaded via curl.exe
- Two sessions compared: tee (local account) vs AzureAD\WaleIbrahim (Entra standard user)

## Risk register - 7 findings (docs/risk-register.md)

| Risk | Severity | Finding | Status |
|---|---|---|---|
| RISK-01 | Critical | No endpoint protection - payload executed silently | Open (partial mitigation) |
| RISK-02 | Critical | tee escalated to SYSTEM via Named Pipe Impersonation | Remediated |
| RISK-03 | Critical | All 5 local account hashes dumped from SAM | Remediated |
| RISK-04 | High | 3 unpatched CVEs (ms16_016, ms16_032, bypassuac_fodhelper) | Mitigated |
| RISK-05 | Informational | Entra standard user: privilege escalation blocked (positive) | N/A |
| RISK-06 | High | tee already in elevated state | Remediated |
| RISK-07 | Informational | Zero remote-service attack surface (positive) | N/A |

## Hardening applied
- Defender real-time protection policy set via registry
- Windows Updates: KB5120249 + KB5121646 applied
- tee removed from Administrators; wardenix-admin created as replacement local admin

## Re-test results
- getsystem: failed across all 6 techniques (error 1346 - access denied)
- hashdump: blocked (error 1168 - no admin token)
- RISK-02 and RISK-03 confirmed remediated

## Evidence
- docs/screenshots/phase-4-tee-meterpreter-sysinfo-getsystem-hashdump.png
- docs/screenshots/phase-4-tee-bypassuac-fodhelper-already-elevated.png
- docs/screenshots/phase-4-wale-bypassuac-fodhelper-not-in-admins.png
- docs/screenshots/phase-4-wale-getsystem-failed-exploit-suggester.png
- docs/screenshots/phase-4-tee-posthardening-getsystem-hashdump-failed.png
