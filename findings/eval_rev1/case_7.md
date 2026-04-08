# Triage Response

## 1. Severity Classification
**Critical**. A production database server, which normally does not initiate outbound connections, is sending 4.7GB of data to an external destination with a TLS certificate that does not match any authorized services. This strongly indicates an active compromise and potential data exfiltration from a critical asset. ⚠️ Flagged for Human Review: While the indicators are severe, a human analyst should confirm the precise baseline for outbound connections on this specific server and verify the exact nature of the "non-matching TLS certificate" detection during the investigation.

## 2. Recommended Immediate Next Step
Isolate the database server (192.168.12.45) from the network to prevent further data exfiltration and contain potential compromise.

## 3. Drafted Reply to Reporter
N/A — automated alert, no reporter reply needed.
