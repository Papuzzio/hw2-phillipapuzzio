# HW2 - Phillip Apuzzio

## Walkthrough Video

[https://youtu.be/HGDccfyJqlk](https://youtu.be/HGDccfyJqlk)

## Workflow: Security Alert Triage and Response Drafting

### Who the User Is

A security engineer or SOC analyst receiving a high volume of security alerts, phishing reports, and incident notifications daily. They have the expertise to make final decisions but spend significant time drafting repetitive first-response communications and performing initial severity classification before any real investigation begins.

### What Input the System Receives

The raw text of an incoming security alert or employee-reported phishing email, including any available context such as reporter name, affected system, and description of the suspicious activity.

### What Output the System Should Produce

A structured triage response containing three components:

1. **Severity Classification** (Critical, High, Medium, Low) with brief justification
2. **Recommended Immediate Next Step** for the analyst
3. **Drafted Reply** to the original reporter acknowledging receipt and setting expectations

The system should explicitly flag any details it cannot assess and mark those for mandatory human review rather than guessing.

### Why This Task Is Valuable Enough to Automate

Security teams are drowning in alerts. Analyst burnout from repetitive triage is one of the most documented problems in the industry. The bottleneck is not expertise — it is time spent on the first pass before real investigation begins. Automating the initial classification and response draft cuts that overhead significantly, lets analysts focus on actual investigation, and ensures reporters receive faster acknowledgment. Partial automation with human review before sending keeps accountability intact.