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

- [ ] **Phase 0 - Foundation:** threat model, architecture, organization design
- [ ] **Phase 1 - Identity Engineering:** users, groups, and governance as code
- [ ] **Phase 2 - Endpoint:** isolated provisioning, Wazuh agent, Entra device registration
- [ ] **Phase 3 - Network Security Architecture:** management infrastructure, firewall design
- [ ] **Phase 4 - Attack, Risk Assessment & Hardening:** baseline compromise, risk register, remediation, re-test
- [ ] **Phase 5 - Baseline Protection:** Security Defaults across the free tier
- [ ] **Phase 6 - Conditional Access Engineering:** tiered policy design
- [ ] **Phase 7 - Privileged Identity Management:** eligible roles, approval workflow
- [ ] **Phase 8 - Identity Protection:** risk detection and investigation
- [ ] **Phase 9 - Identity Governance:** Access Reviews, Entitlement Management
- [ ] **Phase 10 - Log Pipeline & Multi-Engine Analysis:** correlation across all sources
- [ ] **Phase 11 - SOAR + AI-Assisted Response:** automated playbook, incident narrative

## Getting started

Setup steps are added per phase.

---

*Maintained as a portfolio project demonstrating identity, endpoint, and network security engineering, analysis, and automation.*
