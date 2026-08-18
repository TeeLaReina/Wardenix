# Phase 3 - Network Security Architecture

## Overview
Cloud management infrastructure provisioned and configured - the detection
and response platform everything in Phase 4 reports into.

## Infrastructure
- DigitalOcean droplet: wardenix-management, 46.101.255.225, s-2vcpu-4gb,
  Ubuntu 24.04, Frankfurt - provisioned via OpenTofu
- Cloud firewall built rule-by-rule: SSH (22), Wazuh agent data (1514),
  enrollment (1515), dashboard/HTTPS (443), Shuffle SOAR (3443)
- digitalocean_project_resources block added to main.tf - future rebuilds
  land in Wardenix project automatically
- Docker CE 29.6.1 installed from Docker's official repository

## Wazuh 4.14.6
- All-in-one install (manager, indexer, dashboard)
- Critical fix: port 1515 (enrollment) missing from initial firewall -
  agent started locally but never registered; added and verified
- Wale Ibrahim's endpoint (DESKTOP-K8PDBGH) confirmed active in dashboard

## Suricata 8.0.6
- Installed from OISF PPA (Ubuntu default was 7.0.3 - full generation behind)
- HOME_NET corrected from private-LAN default to actual droplet IPs
  (46.101.255.225/32, 10.114.0.4/32)
- 52,058 Emerging Threats Open rules loaded via suricata-update
- End-to-end alerting verified via testmyids.com - GPL ATTACK_RESPONSE rule
  2100498 triggered and confirmed in eve.json

## FreeRADIUS 3.2.5
- Test user authenticating via radtest
- Real RADIUS traffic captured via tcpdump, analyzed in Wireshark -
  Access-Request and Access-Accept confirmed, password correctly encrypted

## Shuffle SOAR
- Installed via Docker Compose
- Hard OpenSearch bug fixed: bootstrap printed success but hash was never
  written - fixed by generating bcrypt hash via hash.sh and pushing via
  securityadmin.sh directly
- Port 9200 conflict resolved between Wazuh indexer and Shuffle OpenSearch
- Memory tuning: heap reduced from 3072m to 768m for shared 3.8GB droplet
- Dashboard accessible at https://46.101.255.225:3443

## Documentation
- infra/suricata-configuration.md
- infra/freeradius-configuration.md
- infra/shuffle-configuration.md

## Evidence
- docs/screenshots/phase-3-wale-win10-endpoint-on-wazuh.png
- docs/screenshots/phase-3-radius-wireshark-capture.png
