# Triage Response

## 1. Severity Classification
**High**
This is a confirmed phishing attempt targeting credentials, explicitly asking the recipient to reset their password via a look-alike domain (`c0mpany-helpdesk.com`). While the reporter did not click the link, the intent is clear credential theft, posing a significant threat if successful.

⚠️ Flagged for Human Review: Confirm the legitimate domains used by the company for IT support communications to definitively establish `c0mpany-helpdesk.com` as malicious, though it is highly probable given the typo and reporter's observation.

## 2. Recommended Immediate Next Step
Block the domain `c0mpany-helpdesk.com` at the email gateway and web proxy to prevent further delivery of this campaign and access to the phishing site.

## 3. Drafted Reply to Reporter
Subject: Re: Suspicious email received - Your Report Received

Hi John,

Thank you for reporting this suspicious email from 'IT-Support@c0mpany-helpdesk.com'. Your action to not click the link was absolutely correct and very helpful.

We have received your report and are initiating an investigation into this phishing attempt. We will update you once our initial analysis is complete, typically within 24-48 hours.

Thanks,
The Security Team
