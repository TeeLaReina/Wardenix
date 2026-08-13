# Phase 4 - Baseline Risk Register

## Purpose

This register documents every security finding produced by the controlled attack sequence against the unhardened endpoint (`DESKTOP-K8PDBGH`, Wale Ibrahim's Entra-joined Tiny10 machine) before any hardening was applied. Each finding maps to a MITRE ATT&CK technique, a severity rating, and a specific hardening control. The same attack sequence is repeated after hardening to measure actual risk reduction.

## Attack conditions

| Parameter | Value |
|---|---|
| Attacker machine | `kalip` (Kali Purple, `10.10.10.10`) |
| Target machine | `Raavix-Win-Endpoint` (Tiny10, `10.10.10.20`) |
| Network | VirtualBox Internal Network `wardenix-lab` - fully isolated, no internet, no host path |
| Attack tooling | Metasploit Framework (`msfvenom`, `msfconsole`, `exploit/multi/handler`) |
| Payload | `windows/meterpreter/reverse_tcp` |
| Two accounts tested | `DESKTOP-K8PDBGH\tee` (local account) and `AzureAD\WaleIbrahim` (Entra-joined standard user) |
| Snapshot state | `PRE-ATTACK-BASELINE` taken on both VMs before the sequence began |
| Date | 12 August 2026 |

---

## Risk register

### RISK-01 - User execution delivers malware with no endpoint protection

| Field | Detail |
|---|---|
| **ATT&CK Technique** | T1204.002 - User Execution: Malicious File |
| **Severity** | Critical |
| **Accounts affected** | Both `tee` and `AzureAD\WaleIbrahim` |
| **Finding** | A reverse-TCP payload (`update.exe`, 7168 bytes) was hosted via HTTP and downloaded by the endpoint. On execution, a live Meterpreter session was established on both accounts. Windows Defender did not detect, block, or alert on the file at any stage - download, storage, or execution. |
| **Evidence** | `phase-4-tee-meterpreter-sysinfo-getsystem-hashdump.png` |
| **Hardening control** | Enable Windows Defender real-time protection; configure attack surface reduction (ASR) rules to block executable content from untrusted sources |
| **Re-test required** | Yes - same payload, same execution method |

---

### RISK-02 - Local account privilege escalation to SYSTEM (immediate)

| Field | Detail |
|---|---|
| **ATT&CK Technique** | T1134.001 - Access Token Manipulation: Token Impersonation/Theft |
| **Severity** | Critical |
| **Accounts affected** | `tee` (local account) |
| **Finding** | `getsystem` succeeded immediately via Named Pipe Impersonation (In Memory/Admin), technique 1 of 6. A standard-privilege local account escalated to SYSTEM without any additional exploit, UAC bypass, or further user interaction. |
| **Evidence** | `phase-4-tee-meterpreter-sysinfo-getsystem-hashdump.png` |
| **Hardening control** | Restrict local account privileges; review and remove unnecessary local admin membership; apply Windows Updates to patch named-pipe impersonation vulnerabilities |
| **Re-test required** | Yes - `getsystem` on a post-hardening session |

RISK-02 — Post-hardening update (13 Aug 2026)

Status: Remediated

Re-test finding: With tee removed from the local Administrators group, getsystem failed across all six techniques (error 1346 — insufficient privilege). Named Pipe Impersonation, which succeeded in the baseline test, was blocked at the privilege-check stage because tee no longer holds a token that can be impersonated to SYSTEM. The Meterpreter session remained constrained to DESKTOP-K8PDBGH\tee (standard user) throughout.

Evidence: phase-4-tee-posthardening-getsystem-hashdump-failed.png

Residual risk: None. Privilege escalation via this vector requires local admin context.

---

### RISK-03 - Full credential dump from SAM database

| Field | Detail |
|---|---|
| **ATT&CK Technique** | T1003.002 - OS Credential Dumping: Security Account Manager |
| **Severity** | Critical |
| **Accounts affected** | `tee` (local account, via SYSTEM access) |
| **Finding** | Once SYSTEM was obtained, `hashdump` successfully extracted NTLM hashes for all five local accounts: `Administrator`, `DefaultAccount`, `Guest`, `tee`, and `WDAGUtilityAccount`. All credentials on the machine are exposed and could be cracked offline or used in pass-the-hash attacks. |
| **Evidence** | `phase-4-tee-meterpreter-sysinfo-getsystem-hashdump.png` |
| **Hardening control** | Enable Credential Guard where supported; enforce unique, strong local account passwords; disable or rename the built-in Administrator account |
| **Re-test required** | Yes - `hashdump` on a post-hardening session |

RISK-03 — Post-hardening update (13 Aug 2026)

Status: Remediated

Re-test finding: hashdump failed (error 1168 — element not found). Without SYSTEM or administrator-level token, the SAM database is inaccessible. Credential extraction via this technique is no longer possible from tee's session.

Evidence: phase-4-tee-posthardening-getsystem-hashdump-failed.png (same screenshot covers both — hashdump output is on the same frame)

Residual risk: None from this session context. If any local admin account is compromised, the SAM remains reachable — covered as an accepted infrastructure design note since wardenix-admin is the sole remaining local admin.

---

### RISK-04 - Three unpatched local privilege escalation CVEs present

| Field | Detail |
|---|---|
| **ATT&CK Technique** | T1068 - Exploitation for Privilege Escalation |
| **Severity** | High |
| **Accounts affected** | Both sessions (CVEs identified from both `tee` and `AzureAD\WaleIbrahim` sessions) |
| **Finding** | `local_exploit_suggester` identified three modules flagged as potentially vulnerable: `ms16_016_webdav`, `ms16_032_secondary_logon_handle_privesc`, and `bypassuac_fodhelper`. These represent independent privilege escalation paths beyond what `getsystem` used - meaning even if one path is patched, others remain. |
| **Evidence** | `phase-4-tee-meterpreter-sysinfo-getsystem-hashdump.png`, `phase-4-wale-getsystem-failed-exploit-suggester.png` |
| **Hardening control** | Apply all outstanding Windows Updates; verify the three named CVEs are patched before re-test |
| **Re-test required** | Yes - `local_exploit_suggester` post-patching |

---

### RISK-05 - Entra-joined standard user: privilege escalation blocked (positive finding)

| Field | Detail |
|---|---|
| **ATT&CK Technique** | T1134.001 - Access Token Manipulation (attempted, failed) |
| **Severity** | Informational (positive control) |
| **Accounts affected** | `AzureAD\WaleIbrahim` |
| **Finding** | Under Wale Ibrahim's Entra-joined standard user account, `getsystem` failed across all six techniques (error 1346). `hashdump` was also blocked (error 1168, directly caused by `getsystem` failing). `bypassuac_fodhelper` additionally confirmed "Not in admins group, cannot escalate" - a separate, explicit boundary. The same payload that gave immediate SYSTEM on a local account produced only a contained standard-user foothold on the Entra-joined account. |
| **Evidence** | `phase-4-wale-getsystem-failed-exploit-suggester.png`, `phase-4-wale-bypassuac-fodhelper-not-in-admins.png` |
| **Hardening control** | No remediation required - this is the expected and correct behaviour. Maintain Entra join and avoid adding the Entra user to the local Administrators group. |
| **Re-test required** | Yes - confirm this boundary still holds post-hardening |

---

### RISK-06 - Local account (`tee`) already in elevated state

| Field | Detail |
|---|---|
| **ATT&CK Technique** | T1078.001 - Valid Accounts: Default Accounts |
| **Severity** | High |
| **Accounts affected** | `tee` (local account) |
| **Finding** | `bypassuac_fodhelper` reported "Already in elevated state" when run against `tee`'s session - confirming this local account runs with elevated privileges by default, making UAC bypass unnecessary. A compromised `tee` account requires no further escalation step to reach administrative capability. |
| **Evidence** | `phase-4-tee-bypassuac-fodhelper-already-elevated.png` |
| **Hardening control** | Review and remove `tee`'s elevated privilege; run all local accounts as standard users by default; require explicit UAC elevation for administrative tasks |
| **Re-test required** | Yes - confirm `tee` no longer starts in elevated state post-hardening |

---

### RISK-07 - Zero remote-service attack surface (positive finding)

| Field | Detail |
|---|---|
| **ATT&CK Technique** | - |
| **Severity** | Informational (positive control) |
| **Finding** | Nmap scanned all 1000 common ports against `10.10.10.20` - every port reported as filtered (no response), not closed. No service is exposed for remote exploitation. The only viable attack path was user-execution, not remote-service exploitation. This is an inherent property of the Tiny10 build combined with the Windows Public firewall profile. |
| **Evidence** | Nmap output captured during reconnaissance stage |
| **Hardening control** | No remediation required - maintain default-deny inbound posture |
| **Re-test required** | No |

---

## Hardening plan (actions to take before re-test)

Based on the above findings, in priority order:

1. **Enable Windows Defender real-time protection** - closes RISK-01
2. **Apply all outstanding Windows Updates** - closes RISK-04 (CVEs)
3. **Remove `tee`'s elevated privileges** - closes RISK-06
4. **Configure Windows Defender ASR rules** - deepens RISK-01 remediation
5. **Re-run the full attack sequence** - validates all of the above

## Re-test baseline

Every finding marked "Re-test required: Yes" must be attempted again post-hardening, using the same payload, the same listener configuration, and the same account. Only failures (payload blocked, privilege escalation denied) count as remediated - partial or inconsistent results require additional hardening.
