# Wardenix Incident Response Runbook
## Compromised Entra ID Account

**Severity:** High / Critical
**Trigger:** Identity Protection high-risk user OR anomalous sign-in detection
**Last updated:** August 2026

---

## Roles

| Role | Responsibility |
|---|---|
| IT Admin 1 (Wale Ibrahim) | Primary responder — account containment |
| IT Admin 2 (Mei Chen) | PIM approver — secondary responder |
| Admin (YetundeDuze) | Escalation, final decisions |

---

## Phase 1 — Detect (0-5 minutes)

1. Alert fires in #wardenix-alerts (Shuffle SOAR) or Grafana Identity Risk Events panel
2. Confirm the alert is real — check ID Protection -> Risky Sign-ins for supporting evidence
3. Note: UPN, userId, IP address, location, risk event type, timestamp
4. If automated response already fired (GitHub issue created), confirm all 8 nodes succeeded

---

## Phase 2 — Contain (5-15 minutes)

**If automated response DID fire:** Verify containment (step below). Skip manual steps.

**If automated response did NOT fire (manual containment required):**

Get a Graph API token first:
```
POST https://login.microsoftonline.com/TENANT_ID/oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

client_id=CLIENT_ID&client_secret=CLIENT_SECRET&scope=https://graph.microsoft.com/.default&grant_type=client_credentials
```

Confirm user compromised:
```
POST https://graph.microsoft.com/v1.0/identityProtection/riskyUsers/confirmCompromised
Authorization: Bearer TOKEN
Content-Type: application/json

{"userIds":["USER_OBJECT_ID"]}
```
Expected: HTTP 204

Revoke all active sessions:
```
POST https://graph.microsoft.com/v1.0/users/USER_OBJECT_ID/revokeSignInSessions
Authorization: Bearer TOKEN
```
Expected: HTTP 200

Block IP at perimeter (SSH to wardenix-management droplet):
```bash
ufw deny from ATTACKER_IP to any
ufw status numbered  # confirm rule is listed
```

**Verify containment:**
- Entra ID -> Risky Users -> confirm status shows "Confirmed compromised"
- UFW status numbered -> confirm deny rule is active

---

## Phase 3 — Investigate (15-60 minutes)

Run these KQL queries in Log Analytics (wardenix-sentinel):

**All sign-ins for the affected user in last 30 days:**
```
AADNonInteractiveUserSignInLogs
| where UserPrincipalName == "UPN_HERE"
| where TimeGenerated > ago(30d)
| project TimeGenerated, IPAddress, Location, ConditionalAccessStatus, AuthenticationRequirement
| order by TimeGenerated desc
```

**PIM activations by the affected user:**
```
AuditLogs
| where TimeGenerated > ago(30d)
| where Category == "RoleManagement"
| where InitiatedBy contains "UPN_HERE"
| project TimeGenerated, OperationName, TargetResources
```

**Any admin actions during the compromise window:**
```
AuditLogs
| where TimeGenerated between (START_TIMESTAMP .. END_TIMESTAMP)
| where InitiatedBy contains "UPN_HERE"
| project TimeGenerated, OperationName, TargetResources, Result
```

**Wazuh alerts from the same time window:**
```
WazuhAlerts_CL
| where TimeGenerated between (START_TIMESTAMP .. END_TIMESTAMP)
| project TimeGenerated, agent_name_s, rule_description_s, rule_level_d
| order by TimeGenerated desc
```

**Questions to answer:**
- How long was the account active before detection?
- Were any PIM roles activated during the compromise window?
- Were any users created, modified, or deleted?
- Were any group memberships changed?
- Did the attacker access any sensitive resources?
- Does Wazuh show any anomalous endpoint activity during the same window?

---

## Phase 4 — Remediate (60-120 minutes)

1. Reset compromised account password — force change on next login
2. Re-enable account after password reset (if account was disabled during containment)
3. Review and revoke any OAuth tokens or app consents granted during the compromise window
4. Patch the entry point — if phishing, block sender domain; if credential stuffing, enforce MFA everywhere
5. Check PIM activation history — if attacker activated a privileged role, review all actions taken during that activation window
6. Clear risk state — ID Protection -> Risky Users -> Confirm user safe (ONLY after full remediation is confirmed)

---

## Phase 5 — Document (ongoing)

- GitHub issue created automatically by Shuffle SOAR (check TeeLaReina/Wardenix repo)
- Update the issue with investigation findings and remediation steps taken
- Add to risk register if a new risk vector was identified
- Schedule post-incident review within 48 hours
- Update KQL detection queries if new attack pattern was identified

---

## Escalation criteria

Escalate to senior leadership if:
- Attacker activated a PIM-eligible role and performed admin actions
- Attacker modified other user accounts or created new accounts
- Attacker accessed financial, HR, or executive data
- Incident is not contained within 30 minutes of detection
- Multiple accounts show risk indicators simultaneously (coordinated attack)

---

## Manual Graph API reference

**Get user object ID:**
```
GET https://graph.microsoft.com/v1.0/users/UPN_HERE
Authorization: Bearer TOKEN
```
Returns: id field = user object ID (UUID format required for risk endpoints)

**Disable account (block sign-in):**
```
PATCH https://graph.microsoft.com/v1.0/users/USER_OBJECT_ID
Authorization: Bearer TOKEN
Content-Type: application/json

{"accountEnabled": false}
```

**Re-enable account after remediation:**
```
PATCH https://graph.microsoft.com/v1.0/users/USER_OBJECT_ID
Authorization: Bearer TOKEN
Content-Type: application/json

{"accountEnabled": true}
```

**Required app registration permissions:**
- IdentityRiskyUser.ReadWrite.All -- confirmCompromised
- User.ReadWrite.All -- account enable/disable
- Directory.ReadWrite.All -- revokeSignInSessions
