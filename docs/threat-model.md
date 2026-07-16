# Threat Model

## Why this document exists

Every control in Wardenix traces back to an identified threat. This project spans four domains that are usually threat-modelled separately - identity, endpoint, network, and AI-assisted response - brought together here because that integration is the actual point of the project.

## Method

**STRIDE** enumerates six threat categories per component: **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure, **D**enial of service, **E**levation of privilege. Each threat maps to a **MITRE ATT&CK** technique and pairs a preventative **control** with a **detection**.

## Assets

| ID | Asset | Why it matters |
|---|---|---|
| A1 | Entra ID tenant | The identity plane for the entire simulated organization |
| A2 | Privileged accounts | 2 PIM-eligible admins, 3 standing P2 users, 1 break-glass account |
| A3 | Tiny10 endpoint | The only real, attackable host in the environment |
| A4 | Network security stack | Wazuh manager, Suricata, RADIUS - the management infrastructure itself |
| A5 | Correlation & log pipeline | Cross-domain visibility; if blinded, nothing downstream works |
| A6 | SOAR + AI triage | Automated response capability and the data it processes |
| A7 | The host machine | Not part of the lab, but adjacent to it - must remain provably isolated |
| A8 | Secrets & credentials | Graph API tokens, SMTP credentials, VirusTotal key, Gemini key, Slack webhook URL |

## Threat register

### A1 - Entra ID tenant

| STRIDE | Threat | ATT&CK | Control | Detection |
|---|---|---|---|---|
| Spoofing | Consent phishing - malicious app tricks a user into granting OAuth permissions | T1528 | Admin consent workflow required for new app permissions | Audit log review of app consent grants |
| Elevation of privilege | Standing admin role assigned instead of PIM-eligible | T1078.004 | Zero standing privileged roles outside the break-glass account | Periodic role assignment audit |
| Tampering | Conditional Access policy silently disabled or weakened | T1556 | Change requires a role only the break-glass account and PIM-eligible admins hold | Audit log alert on CA policy modification |

### A2 - Privileged accounts

| STRIDE | Threat | ATT&CK | Control | Detection |
|---|---|---|---|---|
| Elevation of privilege | Compromised standing account used for lateral movement | T1078 | Only 3 of 6 P2 users hold standing roles; IT Admins are PIM-eligible, not standing | Identity Protection risk-based sign-in |
| Denial of service | Break-glass account itself locked out or disabled by a misapplied policy | T1531 | Explicitly excluded from every Conditional Access policy, documented and tested via What-If | Sign-in monitoring specifically on the break-glass account - any use at all is itself an alert-worthy event |

### A3 - Tiny10 endpoint

| STRIDE | Threat | ATT&CK | Control | Detection |
|---|---|---|---|---|
| Tampering | Exploitation via Metasploit leading to code execution | T1190 / varies by module | Isolated network, snapshot baseline before attack, host firewall tightened post-assessment | Wazuh FIM, active response, Windows Event Log |
| Elevation of privilege | Local privilege escalation post-exploitation | T1068 | Endpoint hardening applied in Phase 4 after baseline risk assessment | Wazuh rootcheck, privilege escalation indicators |
| Credential access | Attempt to extract cached credentials that could reach the identity plane | T1003 | Device-compliance Conditional Access policy limits what a compromised endpoint's credentials can actually do | Wazuh + Identity Protection correlated alert |

### A4 - Network security stack

| STRIDE | Threat | ATT&CK | Control | Detection |
|---|---|---|---|---|
| Elevation of privilege | Management droplet (Wazuh manager, Suricata, Shuffle) exposed to the internet | T1133 | Cloud firewall restricts inbound to the minimum required; admin interfaces never public | CSPM-style check on the droplet's firewall rules |
| Spoofing | RADIUS credential interception on the test network | T1557 | RADIUS traffic confined to the isolated internal segment only | Wireshark capture review, Suricata signature match |

### A5 - Correlation & log pipeline

| STRIDE | Threat | ATT&CK | Control | Detection |
|---|---|---|---|---|
| Denial of service | A log source goes silent and correlation loses visibility without anyone noticing | T1489 | Health checks per source | Log-source-silence alert - fires when an expected source stops reporting |
| Repudiation | Clock drift between Entra, Wazuh, and Suricata makes correlated timelines unreliable | - | Time sync verified across every component before correlation testing | Periodic timestamp-drift check |

### A6 - SOAR + AI triage

| STRIDE | Threat | ATT&CK / class | Control | Detection |
|---|---|---|---|---|
| Tampering | Prompt injection via attacker-influenced text inside alert data reaching the AI model | LLM01 | All input treated as untrusted; the model suggests a response, never executes one | Compare AI-suggested severity against rule-based severity as a sanity check |
| Information disclosure | Internal identifiers (IPs, usernames) sent to an external API unnecessarily | T1552 | Redaction applied before anything leaves the environment | Review of what the triage step actually transmits |
| Elevation of privilege | A Shuffle playbook takes an action beyond its intended scope | - | Playbook actions scoped to least privilege via a dedicated Graph API app registration, not an admin account | Audit log review of actions taken by the automation identity |

### A7 - The host machine

| STRIDE | Threat | ATT&CK | Control | Detection |
|---|---|---|---|---|
| Tampering | Exploit traffic or a compromised VM reaches the host via a misconfigured network adapter | T1210 (lateral movement, adjacent context) | No Bridged or Host-Only adapters anywhere in the project; Internal Network and NAT only; shared folders and clipboard disabled on every VM | Manual verification of adapter configuration before each session; this is the one control in this project with no automated detection - it is verified by process, not tooling |

### A8 - Secrets & credentials

| STRIDE | Threat | ATT&CK | Control | Detection |
|---|---|---|---|---|
| Information disclosure | A token or API key committed to git | T1552.001 | `.gitignore` from the first commit; secret-scanning CI gate | Pipeline failure before merge |

## Residual risk & assumptions

- This is a portfolio lab built for controlled exploitation, not a production identity environment.
- The Entra ID P2 trial is time-bound; PIM and Identity Protection features depend on it remaining active for the phases that use them.
- A7's control is process-based, not automated - this is stated plainly rather than implying a false sense of tooling-backed certainty.

## How this drives the build

- **Phase 1** implements A1 controls (identity architecture, least-privilege role design)
- **Phase 2** implements A3 and A7 controls together - endpoint provisioning cannot happen before isolation is verified
- **Phase 3** implements A4 controls
- **Phase 4** proves A3's threats are real, then remediates them - attack before harden, by design
- **Phases 5–9** implement the remaining A1/A2 controls in depth
- **Phase 10** implements A5 controls
- **Phase 11** implements A6 controls
