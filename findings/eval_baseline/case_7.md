# Triage Response

## 1. Severity Classification
**Critical**
A production database server, which typically should not initiate outgoing connections, is observed exfiltrating a significant volume (4.7GB) of data to an external destination with an unauthorized TLS certificate. This strongly indicates a potential compromise and data exfiltration from a critical asset.

## 2. Recommended Immediate Next Step
Isolate the source host (192.168.12.45) from the network to stop ongoing data exfiltration and prevent further compromise.

## 3. Drafted Reply to Reporter
N/A — automated alert, no reporter reply needed.
