# Triage Response

## 1. Severity Classification
**High**
This alert indicates a sustained brute-force attack (847 attempts in 15 minutes) against the VPN Gateway, a critical access point, targeting the 'admin' user. The source IP is identified as a known Tor exit node, which is a strong indicator of malicious intent, despite no successful logins being detected.

## 2. Recommended Immediate Next Step
Block the source IP `203.0.113.47` at the perimeter firewall or VPN Gateway to prevent further brute-force attempts.

## 3. Drafted Reply to Reporter
N/A — automated alert, no reporter reply needed.
