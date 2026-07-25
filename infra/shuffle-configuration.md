# Shuffle SOAR Configuration

## What this covers

Shuffle runs on the management droplet as the SOAR (Security Orchestration, Automation, and Response) layer - the piece that eventually turns a correlated alert into an automated response, rather than just a notification.

## Version

Installed via a direct clone of the actively-maintained repository rather than pinned to an older tag. Shuffle's own docs state that versions before 2.1.1 lost support in January 2026, with new enforced differences between the Open Source and Enterprise editions, pinning backward risked landing on something now explicitly unsupported, not just outdated.

## Docker

Installed Docker CE 29.6.1 from Docker's official repository, not Ubuntu's `docker.io` package or snap, matching the pattern already established for OpenTofu and other tooling in this project. Snap-packaged Docker has a known socket-path and tooling compatibility issues.

## Port: 3001 → 3443 (HTTPS only)

Shuffle's frontend exposes both HTTP (3001) and HTTPS (3443) by default. Since this identity will eventually hold real Microsoft Graph API automation credentials (Phase 11), only 3443 was opened in the firewall, and 3001 was closed rather than left available alongside it.

## Port conflict: 9200

Shuffle's own `opensearch` container and Wazuh's separate OpenSearch-based indexer both default to port 9200 on the same droplet. Resolved by removing the host-facing port mapping from Shuffle's opensearch service entirely since it's only ever reached internally by Shuffle's own backend and frontend over Docker's private network, never externally.

## Memory sizing

The default `OPENSEARCH_JAVA_OPTS` heap (3072m) was calculated for a 6GB host. This droplet runs 3.8GB total, shared with Wazuh, Suricata, and FreeRADIUS. The default heap caused an out-of-memory kill (exit code 137, confirmed via `docker stats` and system memory pressure). So it was reduced to 768m, which stabilized memory system-wide.

## Authentication failure - a genuine upstream OpenSearch bug

The hardest issue: `backend` could never complete its database handshake, consistently failing with `invalid character 'U' looking for beginning of value` - the literal text `Unauthorized` being returned where JSON was expected.

There were two stacked causes, not one:

1. **A quoted password value.** An early edit left `OPENSEARCH_INITIAL_ADMIN_PASSWORD` wrapped in literal quote characters inside `docker-compose.yml`. Compose doesn't strip these so they became part of the actual password OpenSearch stored, while `backend`'s copy of the same password had no quotes. A straightforward mismatch, but only half the story.

2. **A genuine, documented upstream bug.** Even after removing the quotes and fully wiping the OpenSearch data volume to force clean re-initialization, the failure persisted. OpenSearch's own installer printed `Admin password set successfully`, misleadingly. Directly comparing the stored hash in `internal_users.yml` against a hash generated from the intended password proved they didn't match: the `admin` user's hash was still OpenSearch's stock demo hash, never actually replaced. This is a known, currently-unresolved issue in OpenSearch's Docker security-plugin bootstrap, not a configuration mistake.

## Fix

I bypassed the broken automated bootstrap entirely:

1. Generated a correct bcrypt hash directly: `hash.sh -p '<password>'`
2. Manually replaced the `admin` user's hash in `internal_users.yml` with the correct one
3. Pushed the corrected config into OpenSearch's live security index via `securityadmin.sh`
4. Verified directly against OpenSearch with `curl`, independent of Shuffle's own UI, before trusting the fix

## Note for future rebuilds

Because the root cause is an upstream bug rather than a one-time mistake, it will very likely resurface if the OpenSearch data volume is ever wiped and reinitialized again, for example, a future factory rebuild of this droplet. The hash-patching steps above are the fix to reapply each time; the quoting fix only needed doing once, since it's a permanent file edit.
