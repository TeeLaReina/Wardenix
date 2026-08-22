# Crisis Communication Template
## Compromised Account / Active Security Incident

**Last updated:** August 2026

---

## Automated internal notification (immediate — fired by Shuffle SOAR)

**Channel:** #wardenix-alerts (Slack)
**Audience:** IT Admin team
**Timing:** Automatically within ~20 seconds of detection

Template (sent by Slack_Alert node):
```
SECURITY ALERT - HIGH RISK SIGN-IN DETECTED
User: [UPN]
Risk Level: [riskLevel]
Event Type: [riskEventType]
IP Address: [ipAddress]
Location: [location]
Timestamp: [timestamp]

AI Triage: [severity] - [reason]
Recommended Action: [action]

Actions taken automatically:
[check] User confirmed compromised in Entra ID
[check] IP [ipAddress] blocked in UFW
[check] IR ticket: [github_issue_url]
```

---

## Manual internal escalation (within 30 minutes if escalation criteria met)

**Channel:** Direct message to department head / IT lead
**Sender:** IT Admin 1 (Wale Ibrahim) or Admin (YetundeDuze)
**Timing:** Only if escalation criteria are met (see IR runbook)

---

Subject: Security Incident - Active Investigation

We are currently investigating a security incident involving a potentially compromised
account. Immediate containment actions have been taken automatically.

Status: Under active investigation
Affected account: [NAME/ROLE - not UPN in management comms]
Containment: Account access suspended pending investigation
Expected update: Within [X] hours

No action required from you at this time. We will notify you if the situation
requires escalation or if any data exposure is confirmed.

---

## Post-incident summary (within 24 hours of resolution)

**Audience:** Management, affected user's department head
**Sender:** YetundeDuze (Admin)

---

SECURITY INCIDENT SUMMARY - [DATE]

Incident type: Compromised user account
Detection method: Automated risk detection (Microsoft Identity Protection + Shuffle SOAR)
Time to detection: [X] minutes
Time to containment: [X] minutes (automated) / [X] minutes (manual verification)
Time to resolution: [X] hours

What happened:
A user account showed signs of unauthorized access from an unusual location. Our
automated security system detected and responded to the event without requiring manual
intervention. The account was suspended and the attacker's access point was blocked
within 20 seconds of detection.

Impact:
[Select one:]
- No data exposure confirmed. Investigation complete.
- Investigation ongoing. No confirmed data exposure at this time.
- Data exposure confirmed: [describe scope without technical details]

Actions taken:
- Account suspended immediately on detection
- Attacker network address blocked at perimeter
- All active sessions revoked
- Password reset enforced on next login
- [Add any additional remediation steps]

Preventive measures going forward:
[Specific changes made as a result of this incident]

Status: RESOLVED / ONGOING

---

## What NOT to say

- Do not name the specific user account in management or external communication
- Do not share IP addresses, technical indicators, or investigation details externally
- Do not confirm or deny whether specific data was accessed until investigation is complete
- Do not say "we were hacked" -- say "we detected and responded to a security event"
- Do not discuss the specific tools or detection methods used (operational security)
- Do not share the GitHub issue URL externally -- it is an internal IR record

---

## If the press or external parties ask

Do not respond directly. Escalate to YetundeDuze (Admin) immediately.

Holding statement (to be used only with explicit approval):
"We take the security of our systems and data seriously. We are aware of the matter
and are working to address it. We will provide updates as appropriate."
