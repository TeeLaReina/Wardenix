# Phase 11 — SOAR + AI-Assisted Response (Capstone)

## Overview

8-node Shuffle SOAR workflow that automatically responds to high-risk Entra ID
sign-in events — confirmed compromised in Entra, blocked at the network perimeter,
notified via Slack with structured AI triage, and logged as a GitHub issue.
Built and validated through 21 iterations over 19-21 August 2026.

## Workflow: Wardenix Risky Sign-in Response

### Architecture

```
[TRIGGER] Sentinel_Risky_Signin (Webhook)
        |
[1] Parse_Signin_Data -- extract 7 fields from payload
        |
[2] Gemini -- AI triage: severity, reason, recommended action
        |
[3] Parse_Gemini -- extract clean JSON, strip thoughtSignature blob
        | [condition: action contains "Confirm Compromised"]
[4] Get_Graph_Token -- OAuth2 client credentials Bearer token
        |
[5] Confirm_Compromised -- Graph API: mark user compromised in Entra ID
        |
[6] Block_IP_via_UFW -- SSH to droplet, deny attacker IP in UFW
        |
[7] Slack_Alert -- structured alert to #wardenix-alerts
        |
[8] GitHub_Issue -- automated IR ticket in TeeLaReina/Wardenix
```

### Test payload (used for validation)

```json
{
  "userPrincipalName": "wale.ibrahim@wardenix.onmicrosoft.com",
  "userId": "a456d583-2cae-4b60-8741-cb5bed854dbd",
  "riskLevel": "high",
  "riskEventType": "unfamiliarFeatures",
  "ipAddress": "185.220.101.45",
  "location": "Kyiv, Ukraine",
  "timestamp": "2026-08-19T09:00:00Z"
}
```

Webhook URL:
```
https://46.101.255.225:3443/api/v1/hooks/webhook_45995fda-96bd-45ff-9bea-28e288b3151f
```

---

## Final validated state (21 August 2026, 12:30:41)

| Node | Result | Detail |
|---|---|---|
| Sentinel_Risky_Signin | Triggered | Webhook received, execution started |
| Parse_Signin_Data | Success | 7 fields extracted |
| Gemini | HTTP 200 | severity: Critical, action: Confirm Compromised |
| Parse_Gemini | Success | Clean JSON extracted, thoughtSignature stripped |
| Get_Graph_Token | HTTP 200 | Bearer token, 3599s validity |
| Confirm_Compromised | HTTP 204 | User confirmed compromised in Entra ID |
| Block_IP_via_UFW | success: true | 185.220.101.45 DENY IN confirmed active |
| Slack_Alert | HTTP 200 | Structured alert posted to #wardenix-alerts |
| GitHub_Issue | HTTP 201 | Issue #22 created with clean structured output |

End-to-end execution time: approximately 20 seconds

---

## Problems solved (21 iterations)

### Problem 1 — Docker Swarm inactive
**Symptom:** Executions stuck in EXECUTING indefinitely. Orborus reported
`shuffle_swarm_executions network not found`.

**Fix:**
```bash
docker swarm init --advertise-addr 46.101.255.225
docker network create --driver overlay --attachable shuffle_swarm_executions
docker restart shuffle-orborus
```

### Problem 2 — Gemini model unavailability
**Symptom:** gemini-2.0-flash and gemini-2.5-flash returned 404 — unavailable
to API keys created after a certain date.

**Discovery:** Queried the models endpoint to find available models:
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=KEY" | grep name
```

**Fix:** Switched to gemini-3.5-flash.

### Problem 3 — Gemini 503 / ReadTimeout
**Symptom:** gemini-3.7-flash caused ReadTimeout due to thinking architecture.

**Fix:** Added `"generationConfig":{"thinkingConfig":{"thinkingBudget":0}}` to
disable thinking mode. Set HTTP node timeout to 60 seconds.

### Problem 4 — thoughtSignature blob in output
**Symptom:** Raw Gemini response included massive base64 thoughtSignature making
Slack alerts and GitHub issues unreadable.

**Fix:** Parse_Gemini Python node strips thoughtSignature and extracts clean
severity/reason/action JSON. Falls back gracefully on any parse failure:
```json
{"severity": "System Error", "action": "Manual Analyst Review Required", "reason": "Failed to parse AI response"}
```

### Problem 5 — Shell tilde expansion corrupting client secret
**Symptom:** Client secret contained a `~` character. Shell expanded it as
home directory path, corrupting the secret before it was sent. curl returned
empty output with no error.

**Fix:** URL-encoded `~` as `%7E` in the Shuffle node body field.

### Problem 6 — Invalid userId format
**Symptom:** Confirm_Compromised returned 400 BadRequest "Invalid id format."
Test payload used placeholder `"test-user-id-001"` — not a real Entra UUID.

**Fix:** Retrieved Wale Ibrahim's real object ID via Graph API:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/users/wale.ibrahim@wardenix.onmicrosoft.com" | grep '"id"'
```
Result: `a456d583-2cae-4b60-8741-cb5bed854dbd`

### Problem 7 — Startnode reassignment
**Symptom:** After canvas edits, Shuffle reassigned startnode away from webhook
trigger. All non-trigger nodes showed SKIPPED with "not under the startnode".

**Fix:** Re-clicked webhook trigger to confirm as startnode, re-saved workflow.

### Problem 8 — Condition branch mismatch
**Symptom:** Both branches skipping — "Minimum of one branch's conditions must
be correct to continue. Total: 0 of 1".

**Root cause 1:** Condition source path referenced old node name after rename.
**Fix:** Updated condition to reference `$gemini.body`.

**Root cause 2:** Accidental second connection to Get_Graph_Token — reported
"Skipping due to unfinished parents (1/2)".
**Fix:** Deleted the extra connection.

### Problem 9 — SSH key format incompatibility
**Symptom:** Standard ED25519 OPENSSH key rejected by Shuffle's Paramiko:
`SSHException - unpack requires a buffer of 4 bytes`

**Fix:** Generated a dedicated automation RSA key with no passphrase:
```bash
ssh-keygen -t rsa -b 2048 -m PEM -N '' -f ~/.ssh/wardenix_soar_rsa
```
Public key appended to `/root/.ssh/authorized_keys` on the droplet.

### Problem 10 — UFW command syntax error
**Symptom:** `ufw insert 1 deny from <IP> to any` returned
"ERROR: Invalid position '1'"

**Fix:** `ufw deny from <IP> to any`
(UFW adds deny rules before allow rules by default — explicit position unnecessary)

### Problem 11 — UFW inactive
**Symptom:** Rules were being added but not enforced. `ufw status: inactive`.

**Fix:**
```bash
ufw allow OpenSSH
ufw --force enable
```

### Problem 12 — Wrong webhook URL in Slack_Alert
**Symptom:** Slack_Alert node POSTing to the Shuffle webhook URL instead of
Slack — recursive trigger. The Slack message body appeared as the next payload.

**Fix:** Corrected URL to `https://hooks.slack.com/services/T0BR115H0V9/...`

### Problem 13 — Gemini free tier quota exhausted
**Symptom:** 429 RESOURCE_EXHAUSTED — `quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier`,
quota: 20 requests/day.

**Handling:** Parse_Gemini fallback outputs structured error object. Workflow
continues through all remaining nodes — user still confirmed compromised, IP
blocked, Slack alerted, GitHub issue created. Triage field shows
"System Error — Manual Analyst Review Required".

---

## The 21 iterations

| Stage | Key result | Main issue resolved |
|---|---|---|
| Iterations 1-3 | Webhook fires, executions stuck in EXECUTING | Docker Swarm inactive, shuffle_swarm_executions network missing |
| Iterations 4-6 | Nodes executing but Parse_Signin_Data skipping | Startnode assignment shifting after canvas edits |
| Iterations 7-9 | Gemini 404 on gemini-2.0-flash and gemini-2.5-flash | Model unavailable to new API keys |
| Iterations 10-12 | Gemini 503/timeout | Switched to gemini-3.5-flash with thinkingBudget:0 |
| Iteration 13 | Gemini 200, branch conditions both skipping | Condition source path mismatch after node rename |
| Iteration 14 | Confirm_Compromised 400 | Test userId was a placeholder, not a real UUID |
| Iteration 15 | Confirm_Compromised 204 | First successful Graph API call |
| Iteration 16 | Full chain working, UFW inactive | UFW needed to be enabled on droplet |
| Iteration 17 | Slack firing wrong URL | Slack_Alert URL corrected |
| Iterations 18-19 | Parse_Gemini failing to extract clean text | Python parser refined for edge cases and control characters |
| Iteration 20 | Gemini 429 quota exhausted | Waited for UTC midnight reset, tested with fallback path |
| Iteration 21 | All 8 nodes FINISHED, clean output in Slack and GitHub | Parse_Gemini Python script fully working |

---

## Key architectural decisions

**Identity containment before network isolation:** Confirm_Compromised runs before
Block_IP_via_UFW. Entra risk confirmation triggers CA policies across all cloud
resources immediately — broader and faster than a single firewall rule. The UFW
block is a secondary layer preventing further connection attempts at the perimeter.

**Dedicated automation SSH key:** wardenix_soar_rsa (RSA 2048 PEM, no passphrase)
is scoped strictly to SOAR automation. Cannot be used for interactive admin sessions.
Follows principle of least privilege for automation credentials.

**Graceful degradation on Gemini failure:** Parse_Gemini Python script catches all
exceptions and returns a structured fallback. Gemini outage, quota exhaustion, or
parsing failure does not stop the workflow — user still confirmed compromised, IP
blocked, Slack alerted, GitHub issue created.

**Idempotent UFW rules:** UFW returns "Skipping adding existing rule" when deny
rule already exists. Workflow treats this as success — no errors on re-trigger
for the same IP.

**Microsoft Entra P2 licence note:** The confirmCompromised Graph API endpoint
requires Entra ID P2. In production, P2 licensing must be in place for all accounts
whose risk state the workflow manages.

---

## Infrastructure

| Component | Value |
|---|---|
| Shuffle SOAR | Self-hosted Docker, https://46.101.255.225:3443 |
| Shuffle OpenSearch heap | 512m (reduced from 768m) |
| Docker Swarm | Initialized on management droplet |
| Automation SSH key | wardenix_soar_rsa (RSA 2048 PEM, no passphrase) |
| Slack workspace | Wardenix SOC |
| Slack channel | #wardenix-alerts |
| Gemini model | gemini-3.5-flash (free tier, 20 req/day) |
| Graph API app | wardenix-grafana |

## App registration permissions (wardenix-grafana)

| Permission | Type | Purpose |
|---|---|---|
| User.ReadWrite.All | Application | Account disable/enable |
| IdentityRiskyUser.ReadWrite.All | Application | confirmCompromised endpoint |
| Directory.ReadWrite.All | Application | revokeSignInSessions |
| RoleEligibilitySchedule.Read.Directory | Application | PIM query script (Phase 7) |
| RoleAssignmentSchedule.ReadWrite.Directory | Application | PIM activation history (Phase 7) |

---

## Evidence

### Primary artifacts
- docs/screenshots/phase-11-final-canvas-complete.png
- docs/screenshots/phase-11-full-pipeline-execution.png
- docs/screenshots/phase-11-entra-risky-user-confirmed-compromised.png
- docs/screenshots/phase-11-ufw-block-rule-active.png
- docs/screenshots/phase-11-slack-alert-ai-triage-clean.png
- docs/screenshots/phase-11-github-issue-22-clean-output.png

### Progress artifacts
- docs/screenshots/phase-11-shuffle-workflow-canvas.png
- docs/screenshots/phase-11-entra-risky-users-list.png
- docs/screenshots/phase-11-github-issue-ai-triage-unformatted-v1.png
- docs/screenshots/phase-11-slack-alert-fired.png
- docs/screenshots/phase-11-slack-test-message.png
