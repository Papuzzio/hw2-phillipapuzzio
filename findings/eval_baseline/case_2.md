# Triage Response

## 1. Severity Classification
**High**. This alert indicates an active, automated brute-force attack against the VPN Gateway, a critical piece of infrastructure, targeting a common administrative username ('admin'). The use of a known Tor exit node as the source IP further elevates the risk due to the attacker's attempt at anonymity. While no successful logins are reported, the high volume of attempts (847 in 15 minutes) against a critical service warrants immediate attention.

## 2. Recommended Immediate Next Step
Block the source IP (203.0.113.47) at the perimeter firewall or VPN Gateway to prevent further brute-force attempts.

## 3. Drafted Reply to Reporter
N/A — automated alert, no reporter reply needed.
