# Wardenix

**An identity, endpoint, and network security engineering platform.**

Wardenix provisions and secures a simulated organization end to end: identity architecture on Microsoft Entra ID, an isolated endpoint under real attack, a network security stack watching both, and an AI-assisted response layer tying it together. Every control exists because a specific threat justified it.

> Part of the **Nullfront** project family.

---

## The problem this solves

Identity is the most common initial access vector in modern breaches, and most organizations run it with either too little control (no PIM, no risk-based policy) or too much friction (blanket premium licensing, no scoping). Endpoints and networks are usually defended by separate teams using separate tools that rarely correlate. Wardenix is a working answer to both - one person designing identity governance, endpoint defence, and network detection as a single coherent system, and proving it works by attacking it.

## What this project demonstrates

| Capability | Discipline |
|---|---|
| Identity architecture as code (Microsoft Graph API, PowerShell SDK) | Security Engineering |
| Conditional Access, PIM, and Identity Governance design | Security Engineering |
| Isolated endpoint provisioning and hardening | Security Engineering |
| Network security architecture (firewall design across three layers) | Security Engineering |
| Risk assessment and vulnerability lifecycle management | Security Analysis |
| Identity Protection risk investigation | Security Analysis |
| Multi-engine detection correlation (cloud + endpoint + network) | Security Analysis |
| SOAR playbook design and AI-assisted triage | DevSecOps |
| Secure scripting and CI-gated automation | DevSecOps |
| Threat modelling (STRIDE + ATT&CK across four domains) | Both |

## Architecture

Full system design and data flow: **[docs/architecture.md](docs/architecture.md)**

## Threat model

Every control traces back to an identified threat, across identity, endpoint, network, and AI: **[docs/threat-model.md](docs/threat-model.md)**

## The simulated organization

26 fictional accounts across departments, split by licensing tier deliberately - most run on Entra ID's free baseline, a small privileged subset runs on Premium P2. That split is itself a design decision, not a shortcut: licensing only where the capability is actually needed.

| Tier | Count | Roles |
|---|---|---|
| Entra ID Free (Security Defaults) | 20 | Marketing, Sales, Procurement, general staff, contractors |
| Entra ID P2 | 6 | 2 IT Admins (PIM-eligible), CEO, CFO, HR Lead, Break-Glass Admin |

## Technology stack

| Layer | Tool |
|---|---|
| Identity | Microsoft Entra ID (P2), Graph API, Graph PowerShell SDK |
| Endpoint | Local isolated VM (Tiny10), Wazuh agent |
| Network security | Wazuh manager, Suricata, NPS/RADIUS, Wireshark |
| Adversary emulation | Metasploit Framework |
| Detection-as-code | Sigma, KQL |
| Log pipeline | Azure Log Analytics, Grafana Cloud, Azure Monitor Workbooks |
| SOAR | Shuffle (self-hosted) |
| Alerting & notifications | Slack (via Grafana Alerting) |
| AI-assisted triage | Google Gemini API |
| Infrastructure-as-Code | OpenTofu |
| Automation & CI | GitHub Actions, Python, PowerShell |

## Design principle: the host machine is never part of the lab

Every VM in this project runs on isolated virtual networking with no path back to the machine building it. This isn't incidental - it's a deliberate boundary documented and enforced before any attack tooling runs. Detail in the architecture doc's trust boundaries section.

## Roadmap

- [x] **Phase 0 - Foundation:** threat model, architecture, organization design
- [x] **Phase 1 - Identity Engineering:** users, groups, and governance as code
#### Phase 1 - 26 users and 11 dynamic groups, provisioned entirely via Microsoft Graph API

![26 users provisioned via Graph API script](docs/screenshots/phase-1-users-provisioned.png)
- [x] **Phase 2 — Endpoint:** isolated provisioning, Entra device registration (Wazuh agent deferred to Phase 3 — requires a live manager to connect to)

#### Phase 2 — Isolated endpoint, verified network boundaries, cloud-trust registered

![Device registered as Microsoft Entra joined, owned by Wale Ibrahim](docs/screenshots/phase-2-entra-device-joined.png)
- [x] **Phase 3 - Network Security Architecture:** management infrastructure, firewall design

#### Phase 3 — Management infrastructure, network detection, and SOAR

![Wale Ibrahim's endpoint active in Wazuh dashboard](docs/screenshots/phase-3-wazuh-endpoint-active.png)

Built the cloud management infrastructure — the detection and response platform
everything in Phase 4 reports into.

- Management droplet provisioned via OpenTofu on DigitalOcean (Frankfurt, s-2vcpu-4gb, Ubuntu 24.04)
- Cloud firewall built rule-by-rule: SSH (22), Wazuh agent data (1514), enrollment (1515), dashboard (443), Shuffle SOAR (3443)
- **Wazuh 4.14.6** (manager, indexer, dashboard) — Wale Ibrahim's endpoint confirmed active
- Critical fix documented: port 1515 (enrollment) was initially missing — agent started locally but never registered; added and verified
- **Suricata 8.0.6** installed from OISF PPA — HOME_NET corrected from private-LAN default to actual droplet IPs; 52,058 Emerging Threats Open rules loaded; alerting verified via testmyids.com
- **FreeRADIUS 3.2.5** — test user authenticating; real RADIUS traffic captured and analyzed in Wireshark
- **Shuffle SOAR** (self-hosted via Docker) — survived a hard OpenSearch bootstrap bug where the password hash was not written despite a success message; fixed by bypassing the broken installer and writing the hash directly via securityadmin.sh
- Configuration docs committed: `infra/suricata-configuration.md`, `infra/freeradius-configuration.md`, `infra/shuffle-configuration.md`

- [x] **Phase 4 - Attack, Risk Assessment & Hardening:** baseline compromise, risk register, remediation, re-test

#### Phase 4 — Attack, risk assessment, and hardening

![tee session: SYSTEM via Named Pipe Impersonation, all hashes dumped](docs/screenshots/phase-4-tee-meterpreter-sysinfo-getsystem-hashdump.png)
![Wale Ibrahim session: getsystem blocked, hashdump blocked](docs/screenshots/phase-4-wale-getsystem-failed-exploit-suggester.png)

Attacked the unhardened endpoint, formally risk-registered every finding, hardened, then re-tested to measure genuine risk reduction. Attack before harden — always.

**Baseline attack sequence:**
- Static IPs assigned: kalip (attacker) = `10.10.10.10`, endpoint (target) = `10.10.10.20`
- Payload: `windows/meterpreter/reverse_tcp`, delivered via HTTP and user execution (T1204.002)
- Two sessions compared:
  - **`tee` (local account):** `getsystem` succeeded immediately via Named Pipe Impersonation → SYSTEM. All 5 local account hashes dumped. `bypassuac_fodhelper`: already elevated.
  - **`AzureAD\WaleIbrahim` (Entra standard user):** `getsystem` failed across all 6 techniques. `hashdump` blocked. `bypassuac_fodhelper`: not in admins group. Meaningfully more contained blast radius.
- 3 CVEs flagged by `local_exploit_suggester`: `ms16_016`, `ms16_032`, `bypassuac_fodhelper`

**Risk register — 7 findings:** `docs/risk-register.md`

| Risk | Severity | Finding |
|---|---|---|
| RISK-01 | Critical | No endpoint protection — payload executed silently |
| RISK-02 | Critical | Local account escalated to SYSTEM immediately |
| RISK-03 | Critical | All 5 local account hashes dumped from SAM |
| RISK-04 | High | 3 unpatched local privilege escalation CVEs |
| RISK-05 | Informational | Entra standard user: privilege escalation blocked (positive) |
| RISK-06 | High | `tee` account already in elevated state |
| RISK-07 | Informational | Zero remote-service attack surface (positive) |

**Hardening applied:**
- Windows Defender real-time protection policy set via registry (Tiny10 has no Defender GUI)
- Windows Updates applied: KB5120249 + KB5121646 — confirmed up to date
- `tee` removed from Administrators; `wardenix-admin` created as replacement local admin

**Re-test:** same payload re-run post-hardening against both accounts. Results and updated screenshots committed.

- [x] **Phase 5 - Baseline Protection:** Security Defaults across the free tier

#### Phase 5 — Baseline protection: Security Defaults

![Security Defaults enabled on Wardenix tenant](docs/screenshots/phase-5-security-defaults-enabled.png)

Confirmed and documented the free-tier identity baseline active across all 26 accounts.

- Security Defaults was enabled automatically by Microsoft at tenant creation (confirmed August 2026)
- Enforces: MFA registration for all users, mandatory admin MFA, risk-based user MFA challenges, legacy authentication blocked, device code flow blocked
- Documented Security Defaults vs. Conditional Access trade-offs — Security Defaults is the correct free-tier tool; Phase 6 replaces it with granular CA policies for the 6 P2-licensed accounts

- [x] **Phase 6 - Conditional Access Engineering:** tiered policy design

#### Phase 6 - Conditional Access Engineering

![All 6 CA policies enabled](docs/screenshots/phase-6-ca-policies-all-enabled.png)

Replaced Security Defaults with six scoped CA policies for the 6 P2-licensed accounts. Free-tier 20 users remain under Security Defaults.

- CA-01: MFA required for IT Admins (Wale, Mei) on all resources
- CA-02: MFA required for privileged users (David, Sofia, Ama) on all resources
- CA-03: Legacy authentication blocked - Exchange ActiveSync and Other clients only
- CA-04: MFA required for all 6 P2 users across all cloud apps
- CA-05: MFA step-up on medium and high risk sign-ins (P2 Identity Protection signal)
- CA-06: Entra-joined device required for IT Admin access - enforces DESKTOP-K8PDBGH as the only trusted endpoint
- All policies validated in Report-only mode via What If tool before enabling
- BreakGlass Admin excluded from every policy

- [x] **Phase 7 - Privileged Identity Management:** eligible roles, approval workflow

#### Phase 7 - Privileged Identity Management

![PIM eligible assignments - Wale and Mei](docs/screenshots/phase-7-pim-eligible-assignments.png)

Just-in-time privileged access replacing standing admin rights for both IT Admin accounts.

- Wale Ibrahim: Identity Governance Administrator (eligible) - approver: Mei Chen
- Mei Chen: Cloud Device Administrator (eligible) - approver: Wale Ibrahim
- Role settings: 1-hour max activation, Azure MFA required, justification required, approval required
- Activation workflow validated end-to-end: request → MFA → peer approval → time-bound active role
- Additional finding: CA-06 confirmed blocking sign-in from non-Entra-joined device (AADSTS9001011) - CA-06 set back to Report-only for testing window

- [x] **Phase 8 - Identity Protection:** risk detection and investigation

#### Phase 8 - Identity Protection: Risk Detection and Investigation

![Risk detections - Anonymous IP and Malicious IP, High severity](docs/screenshots/phase-8-risk-detections-tor.png)

Simulated a real attack using Tor Browser, triggered two High-risk detections, investigated across all ID Protection reports, and remediated.

- Tor Browser sign-in attempt as Wale Ibrahim triggered two simultaneous High-risk detections: Anonymous IP address and Malicious IP address
- Microsoft threat intelligence identified the Tor exit node as actively malicious - not just anonymous
- Smart lockout fired before password entry (error 50053) - account locked at network layer
- Wale flagged in Risky users: At risk, High (3.57% of 26-user org)
- CA-05 (MFA on risky sign-ins) confirmed in scope - would have challenged MFA had sign-in completed
- Remediation: Confirm user safe in ID Protection, sessions revoked, risk state cleared

- [ ] **Phase 9 - Identity Governance:** Access Reviews, Entitlement Management
- [ ] **Phase 10 - Log Pipeline & Multi-Engine Analysis:** correlation across all sources
- [ ] **Phase 11 - SOAR + AI-Assisted Response:** automated playbook, incident narrative

## Getting started

Setup steps are added per phase.

---

*Maintained as a portfolio project demonstrating identity, endpoint, and network security engineering, analysis, and automation.*

#### Phase 5 — Baseline protection: Security Defaults

![Security Defaults enabled on Wardenix tenant](docs/screenshots/phase-5-security-defaults-enabled.png)

Confirmed and documented the free-tier identity baseline active across all 26 accounts.

- Security Defaults was enabled automatically by Microsoft at tenant creation (confirmed August 2026)
- Enforces: MFA registration for all users, mandatory admin MFA, risk-based user MFA challenges, legacy authentication blocked, device code flow blocked
- Documented Security Defaults vs. Conditional Access trade-offs — Security Defaults is the correct free-tier tool; Phase 6 replaces it with granular CA policies for the 6 P2-licensed accounts
