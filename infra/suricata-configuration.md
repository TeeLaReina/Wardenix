# Suricata Configuration

## What this covers

Suricata runs on the management droplet as the network-layer detection engine, watching wire traffic directly, independent of what Wazuh sees at the host level. Two engines, two vantage points, same principle as the rest of Wardenix's detection design.

## Version

Ubuntu 24.04's default repository ships Suricata 7.0.3 which is stale, relative to current releases so I installed from the Open Information Security Foundation's own PPA instead (`ppa:oisf/suricata-stable`), landing on version **8.0.6**, the actual current stable release as at the time of install.

```bash
apt remove -y suricata-update  # because the standalone package conflicts with the PPA's bundled version
add-apt-repository ppa:oisf/suricata-stable -y
apt update
apt install -y suricata
```

## Interface

The interface is bound to `eth0`, carrying the droplet's actual public and private traffic. Confirmed via `ip addr show`.

## HOME_NET - the one setting that mattered most

Suricata's default `HOME_NET` ships pre-configured for a private enterprise LAN:

```yaml
# Default (wrong for this deployment)
HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"
```

None of those ranges include this droplet's actual address. A large share of the Emerging Threats rule set keys off `HOME_NET` to distinguish genuine inbound attacks (external → protected asset) from background noise - leaving the default in place would have silently degraded detection quality without any error or warning to indicate it.

So I corrected to the droplet's real addresses, scoped precisely rather than left broad:

```yaml
HOME_NET: "[46.101.255.225/32,10.114.0.4/32]"
#HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"  # original default, kept for reference
```

`/32` on each - single host, not a range - following the same least-privilege reasoning applied to network detection as everywhere else in this project.

## Rule set

The ruleset was loaded via `suricata-update`, defaulting to **Emerging Threats Open** - a free, actively maintained signature set covering known exploit patterns, scanning tools, and malicious traffic behaviors. 52,058 rules loaded and validated (`suricata -T`) before going live.

## Verification

Passive parsing confirmed first - a live external SSH handshake against the droplet was correctly logged with full protocol detail (client/server version strings) in `eve.json`, proving packet capture and protocol parsing were both functioning.

Active alerting confirmed second, using the industry-standard IDS test endpoint:

```bash
curl http://testmyids.com
```

Produced a genuine matched alert:

```json
"signature":"GPL ATTACK_RESPONSE id check returned root"
"signature_id":2100498
"category":"Potentially Bad Traffic"
```

All this confirms the full chain - capture, parsing, rule matching, structured alert output - are working end to end.
