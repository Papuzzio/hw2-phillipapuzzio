# Report

## 1. Business Use Case

The prototype automates first-pass triage of security alerts and employee-reported phishing emails for SOC analysts. Input is the raw text of an alert — reporter name, affected system, description of suspicious activity. Output is a structured response with three sections: a severity classification (Critical/High/Medium/Low) with justification, a single recommended next step, and a drafted reply to the reporter. The system flags any details it cannot assess for mandatory human review rather than guessing.

The target user is a security engineer or SOC analyst who receives a high volume of alerts daily. They have the expertise to make final decisions but spend significant time on repetitive first-response drafting and initial severity classification before real investigation begins. Analyst burnout from this overhead is well-documented. The bottleneck is time, not expertise. Automating the initial classification and response draft cuts that overhead, lets analysts focus on investigation, and ensures reporters receive faster acknowledgment.

## 2. Model Choice

The prototype uses **Gemini 2.5 Flash** via the `google-genai` SDK. Gemini was chosen for three reasons: free API tier suitable for a school assignment, fast inference speed appropriate for triage workflows, and the assignment's recommendation to use available free-tier models. Anthropic's Claude was initially implemented but dropped due to cost — the free tier did not provide sufficient quota for iterative evaluation across 7 test cases and 3 prompt versions.

During Revision 2 evaluation, `gemini-2.5-flash` became unavailable due to API rate limits (503 errors). The remaining cases (2, 3, 4, 5, 7) were run on `gemini-2.5-flash-lite` instead. This forced model switch is a confound in the Rev2 results, particularly for Case 7, where severity dropped from Critical to High. That regression cannot be cleanly attributed to the prompt change alone.

## 3. Baseline vs. Final Design Comparison

Three cases showed the clearest improvement across prompt revisions:

| Case | Baseline Behavior | Final (Rev2) Behavior | Prompt Change That Fixed It |
|------|------------------|----------------------|----------------------------|
| **Case 4** (vague "something weird" report) | Classified **Medium** — model treated vague symptoms as suspicious activity warranting investigation. No Low classification despite zero concrete threat indicators. | Classified **Low** — model correctly identified that "computer is slow" and "a window popped up" are vague symptoms with no specific IOCs. Flagged for human review and recommended gathering more info from the reporter. | Rewrote the Low definition with concrete symptom-level examples (e.g., "computer is slow," "a window popped up") to give the model a clearer anchor for when Low is appropriate. |
| **Case 5** (R&D lab scanning) | Classified **Medium** — model downgraded severity because the R&D lab has authorized pen-testing tools, treating the innocent explanation as grounds to lower classification. | Classified **High** — model recognized the activity could be benign but classified at the higher severity because consequences would be severe if it were not legitimate. | Expanded the High definition to explicitly state: "When an alert contains a plausible innocent explanation but the worst-case scenario is severe, classify High and flag the ambiguity — do NOT downgrade to Medium based on the innocent explanation alone." |
| **Case 6** (BEC wire transfer, $148K) | Classified **Critical** in baseline, then **regressed to High** in Rev1 because the calibration guide's language about "confirmed attack" led the model to anchor on uncertainty about whether the email was spoofed. | Classified **Critical** — model correctly identified the immediate financial risk as the deciding factor, regardless of whether the attack vector was confirmed. | Added "OR any risk of immediate financial loss (e.g., wire transfer requests, BEC)" to the Critical definition, making financial risk an independent trigger for Critical classification. |

Additional stable results: Cases 1 (phishing), 2 (brute force), and 3 (lost laptop) maintained appropriate severity classifications and professional reply drafts across all three prompt versions, confirming that targeted prompt changes fixed specific failures without destabilizing correct behavior elsewhere.

## 4. Remaining Failure Modes

Case 7 (Spanish-language data exfiltration alert) dropped from Critical to High in Rev2, but this coincided with a forced switch from `gemini-2.5-flash` to `gemini-2.5-flash-lite` due to rate limits, so the regression cannot be attributed to the prompt change alone — the smaller model may lack capacity to fully parse non-English technical alerts. Beyond this specific case, the system carries residual risk of severity miscalibration on ambiguous inputs: the calibration guide improved classification accuracy on tested cases, but novel ambiguous scenarios outside the evaluation set may still produce incorrect severity levels. The drafted reply section is another persistent concern — the model cannot verify reporter identity, confirm internal system context, or check whether recommended actions (e.g., remote wipe, IP block) have already been taken. Every reply the model drafts is a suggestion, not a verified communication, and sending it without review could create confusion or expose internal procedures to an attacker who submitted the alert.

## 5. Deployment Recommendation

This system should **not** be deployed as an autonomous triage tool. It should be deployed as an **analyst-assist tool** where every output is reviewed and manually approved before any action is taken. Specifically, the following controls are required:

- **Human-in-the-loop on severity**: An analyst must review and confirm (or override) every severity classification before it is logged in the ticketing system. The model's classification is a starting suggestion, not a final determination.
- **Mandatory sign-off before any reply is sent**: No drafted reply should be sent to a reporter without an analyst reading it, verifying the reporter's identity, and confirming the stated next steps are accurate and appropriate.
- **Drift monitoring**: Log the model's proposed severity alongside the analyst's final decision. Track disagreement rates over time. If the model's accuracy degrades (e.g., due to model updates or changing alert patterns), the calibration guide in the system prompt should be revised using the same evidence-based iteration process documented in `prompts.md`.

Under these conditions, the system provides genuine value: it cuts the time analysts spend on initial drafting, ensures reporters get faster acknowledgment, and standardizes triage output format. Without these controls, it introduces unacceptable risk of misclassification, inappropriate responses, and false confidence in automated security decisions.
