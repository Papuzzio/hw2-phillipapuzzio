#!/usr/bin/env python3
"""
HW2 - Phillip Apuzzio
Security Alert Triage and Response Drafting

Reads a raw security alert or phishing report and produces a structured
triage response using the Google Gemini API.
"""

from __future__ import annotations

import argparse
import os
import sys

from google import genai

SYSTEM_PROMPT = """\
You are a senior SOC (Security Operations Center) analyst assistant. Your job \
is to perform first-pass triage on incoming security alerts and employee-reported \
phishing emails.

Given the raw text of an alert, produce a response with EXACTLY these three \
sections, using the markdown headers shown:

## 1. Severity Classification
Assign one of: **Critical**, **High**, **Medium**, or **Low**.
Follow it with 1-3 sentences justifying the rating based ONLY on concrete \
evidence present in the alert text.

Use this calibration guide:
- **Critical**: Active compromise, data exfiltration, OR any risk of immediate \
  financial loss (e.g., wire transfer requests, BEC). When money or data is at \
  stake right now, always classify Critical.
- **High**: Confirmed attack in progress, credible threat to critical systems, \
  or suspicious activity that COULD be benign but carries serious consequences \
  if it is not. When an alert contains a plausible innocent explanation (e.g., \
  authorized testing) but the worst-case scenario is severe, classify High and \
  flag the ambiguity — do NOT downgrade to Medium based on the innocent \
  explanation alone.
- **Medium**: Suspicious activity with clear technical indicators (e.g., known \
  malicious domain, spoofed sender) but no confirmed compromise and no immediate \
  risk of financial loss or data exfiltration.
- **Low**: Report is vague, contains no specific technical indicators, and \
  describes symptoms that are more likely benign than malicious (e.g., "computer \
  is slow," "a window popped up"). Use Low when the reporter cannot identify \
  what they saw and no concrete IOC is present.

## 2. Recommended Immediate Next Step
Provide exactly ONE concrete action the analyst should take right now. \
Do not list multiple steps. Pick the single most impactful action before \
deeper investigation begins (e.g., block an IP, isolate a host, verify with \
the reporter). If information is too vague to act on, the single next step \
should be to gather more information from the reporter.

## 3. Drafted Reply to Reporter
Write a short, professional email reply to the person who submitted the alert. \
Acknowledge receipt, briefly state what the security team will do next, and set \
a realistic expectation for follow-up timing. If the alert is automated (no \
human reporter), state "N/A — automated alert, no reporter reply needed."

IMPORTANT RULES:
- If any detail is missing, ambiguous, or cannot be reliably assessed from the \
  provided text, you MUST explicitly flag it with a "⚠️ Flagged for Human Review" \
  note in the relevant section explaining what is uncertain and why. Every response \
  should have at least one flag unless every detail is unambiguously clear.
- Be concise. The analyst is busy.
- Do not invent technical details that are not present in the input.
- Always respond in English, even if the input alert is in another language.
"""


def build_prompt(alert_text: str) -> str:
    """Wrap the raw alert text in a clear user message."""
    return (
        "Triage the following security alert:\n\n"
        "---BEGIN ALERT---\n"
        f"{alert_text}\n"
        "---END ALERT---"
    )


def triage(alert_text: str, model: str, persona: str | None = None) -> str:
    """Send the alert to the Gemini API and return the triage response."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    system = SYSTEM_PROMPT
    if persona:
        system += f"\n\nAdditional analyst context: {persona}"

    response = client.models.generate_content(
        model=model,
        contents=build_prompt(alert_text),
        config=genai.types.GenerateContentConfig(
            system_instruction=system,
        ),
    )
    return response.text


def main():
    parser = argparse.ArgumentParser(
        description="Security Alert Triage and Response Drafting"
    )
    parser.add_argument(
        "--input", required=True, help="Path to a text file containing the raw alert"
    )
    parser.add_argument(
        "--output", default=None, help="Optional path to write the triage response (.md)"
    )
    parser.add_argument(
        "--persona",
        default=None,
        help="Optional persona/context string appended to the system prompt",
    )
    parser.add_argument(
        "--model", default="gemini-2.5-flash", help="Gemini model to use"
    )
    args = parser.parse_args()

    # --- Read input ---
    if not os.path.isfile(args.input):
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r") as f:
        alert_text = f.read().strip()

    if not alert_text:
        print("Error: input file is empty", file=sys.stderr)
        sys.exit(1)

    # --- Print input ---
    print("=" * 60)
    print("INPUT ALERT")
    print("=" * 60)
    print(alert_text)
    print()

    # --- Call API ---
    print("Triaging alert with", args.model, "...")
    print()
    response = triage(alert_text, model=args.model, persona=args.persona)

    # --- Print output ---
    print("=" * 60)
    print("TRIAGE RESPONSE")
    print("=" * 60)
    print(response)
    print()

    # --- Optionally write to file ---
    if args.output:
        with open(args.output, "w") as f:
            f.write(f"# Triage Response\n\n{response}\n")
        print(f"Response written to {args.output}")


if __name__ == "__main__":
    main()
