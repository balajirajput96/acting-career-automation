# AI Agent Rules for Acting Career Automation

This document outlines the behavior rules for any AI agents interacting with this repository and its workflows.

## General Principles

*   **Transparency:** All actions taken by AI agents must be transparent and auditable through GitHub logs.
*   **Human Oversight:** AI agents are designed to assist and automate repetitive tasks, but critical decisions and direct communication with external contacts remain under human control.
*   **Security and Privacy:** Agents must adhere to strict security protocols and protect sensitive information.

## Specific Behavioral Rules

1.  **No Automated Direct Messaging (DM) or Emailing:**
    *   AI agents are strictly forbidden from sending direct messages (DMs) or emails to any external contacts.
    *   All generated outreach content (email drafts, DM drafts) must be posted as comments or within the body of GitHub Issues for human review and manual sending.

2.  **No Automatic Issue or Pull Request Closure:**
    *   AI agents must *never* automatically close GitHub Issues or Pull Requests.
    *   The `scripts/reply_processor.py` script, and any other automation, is designed only to apply labels and facilitate movement on the Project board, not to close items.
    *   Issue closure is a manual action reserved for the repository owner.

3.  **Project Board Interaction:**
    *   AI agents may add labels to issues (e.g., `lead-new`, `lead-sent`, `lead-rejected`, `lead-callback`, `follow-up-needed`, `warning`).
    *   AI agents may suggest or facilitate movement of issues between columns on the GitHub Project board (v2) based on applied labels or comment commands (e.g., `/sent`, `/rejected`, `/callback`). However, direct programmatic movement of issues on the project board is currently a placeholder for manual action or requires specific project board automation rules to be set up by the user.

4.  **Scam Red-Flagging:**
    *   The `scripts/parse_leads.py` script, executed by AI agents, will actively check for potential scam indicators in new leads (e.g., requests for fees, use of generic email domains, missing project names).
    *   If red flags are detected, the agent must apply a `warning` label to the corresponding GitHub Issue and include details in the issue body.

5.  **No Unauthorized Modifications:**
    *   AI agents must not modify repository files, workflows, or settings unless explicitly instructed and designed to do so by the repository owner.

By adhering to these rules, AI agents can effectively support the acting career automation workflow while maintaining human control and ensuring ethical interactions.
