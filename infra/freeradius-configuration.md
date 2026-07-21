# FreeRADIUS Configuration

## What this covers

FreeRADIUS runs on the management droplet as a test authentication service, generating real RADIUS protocol traffic for Suricata and Wireshark to observe, distinct from the HTTPS-based traffic every other service in this project produces.

## Version

Ubuntu 24.04's default repository ships 3.2.5 - a few patches behind the true latest (3.2.8), but still the current 3.2.x branch. Since it's not meaningfully stale, I used it as-is rather than adding a separate vendor repository, unlike Wazuh and Suricata where the default was a full generation behind.

## Test user

A single test account exists purely to generate authentication traffic:
**testuser Cleartext-Password := "TestPass123"**

Deliberately simple, not a strong random password - this account protects nothing real; its only purpose is being authenticated against repeatedly during testing and traffic analysis.

## Verification

```bash
radtest testuser TestPass123 localhost 0 testing123
```

It returned a genuine `Access-Accept`, confirming the full authentication chain - request, credential validation, response - working correctly before any Wireshark or Suricata observation work builds on top of it.
