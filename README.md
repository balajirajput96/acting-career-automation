# Acting Career Automation Toolkit

This repository contains a set of Python scripts and GitHub Actions workflows to help actors manage their casting leads, generate personalized outreach drafts, and track follow-ups. This is a GitHub-centric toolkit, not a web dashboard.

## Structure

```
acting-career-automation/
├── README.md                       # Setup + daily workflow guide
├── AGENTS.md                       # AI agents ke liye rules
├── .github/workflows/
│   ├── draft_generator.yml         # Daily CSV read -> new leads Issues
│   ├── follow_up_tracker.yml       # 7-day old 'sent' leads reminder Issue
│   └── reply_processor.yml         # Issue comments (/sent, /rejected, /callback) -> labels + Project board move
├── scripts/
│   ├── generate_drafts.py          # CSV row -> personalized email + DM draft
│   ├── parse_leads.py              # Detect new rows (status=NEW), check scam red-flags
│   ├── tracker_utils.py            # Shared helpers: CSV read/write, GitHub API wrappers
│   └── requirements.txt            # Python dependencies
├── data/
│   ├── casting_leads.csv           # Columns: id,date_found,source,project,role,contact_type,contact,status,notes
│   └── casting_leads.sample.csv    # 2-3 example rows (dummy data)
├── templates/
│   ├── email_template.md           # {{name}}, {{role}}, {{source}}, {{project}} placeholders
│   ├── dm_template.md              # Short IG/WhatsApp version
│   └── followup_template.md        # Polite 7-day follow-up
├── profile_kit/
│   └── CHECKLIST.md                # Headshot/Reel/Monologue/Intro video checklist + shooting tips
└── .gitignore
```

## Setup Instructions

1.  **Create this repository on GitHub:** You've already done this step.

2.  **Upload Files:** Ensure all files from this toolkit are uploaded to your `acting-career-automation` GitHub repository.

3.  **GitHub Token:** The default `GITHUB_TOKEN` provided by GitHub Actions is sufficient for these workflows. No extra secrets are needed.

4.  **Create a GitHub Project Board (v2):**
    *   Go to your repository on GitHub.
    *   Navigate to the "Projects" tab.
    *   Create a new Project (Table layout is recommended).
    *   Add the following four columns:
        *   `New`
        *   `Sent`
        *   `Follow-up`
        *   `Closed-tracking`
    *   (Optional) Configure automation rules for your project board to automatically move issues based on labels (e.g., `lead-new` to `New`, `lead-sent` to `Sent`, etc.). The `scripts/reply_processor.py` script will add labels, but manual project board movement might be needed if automation rules are not set up.

5.  **Start Adding Leads:** Begin adding your casting leads to `data/casting_leads.csv`.

## Daily Workflow

1.  **Add New Leads:** Update `data/casting_leads.csv` with new leads, setting their `status` to `NEW`.

2.  **Automatic Issue Creation:** The `.github/workflows/draft_generator.yml` workflow runs daily (or can be triggered manually). It will:
    *   Read `data/casting_leads.csv`.
    *   Detect leads with `status=NEW`.
    *   Run `scripts/parse_leads.py` to check for scam red-flags (fees, free email domains, missing project names) and add a `warning` label if detected.
    *   Create a new GitHub Issue for each `NEW` lead, labeled `lead-new`.
    *   `scripts/generate_drafts.py` will then add personalized email and DM drafts to the issue body.

3.  **Review and Act on Issues:**
    *   Go to your repository's "Issues" tab.
    *   Review new issues. Check for `warning` labels.
    *   Copy the generated email/DM drafts from the issue body and send them manually.

4.  **Update Lead Status via Comments:** After sending an outreach, or if you get a response, add a comment to the relevant issue with one of the following commands:
    *   `/sent`: Marks the lead as sent. Adds `lead-sent` label, removes `lead-new`.
    *   `/rejected`: Marks the lead as rejected. Adds `lead-rejected` label, removes other lead labels.
    *   `/callback`: Marks the lead for a callback/follow-up. Adds `lead-callback` label, removes `lead-new` or `lead-sent`.
    *   `/followed-up`: Dismisses a follow-up reminder.

5.  **Automatic Follow-up Reminders:** The `.github/workflows/follow_up_tracker.yml` workflow runs daily (or can be triggered manually). It will:
    *   Check `lead-sent` issues.
    *   If an issue was created more than 7 days ago (and hasn't been followed up), it will add a `follow-up-needed` label and a comment reminding you to follow up.

## Automation Control Plane

GitHub is the durable home for repository-local automation. The scheduled workflows keep running when a local terminal session is closed, while the terminal tools use the repository rules and assets below for internal work.

| Asset | Purpose |
| --- | --- |
| `.github/workflows/toolkit_health.yml` | Daily health check for scripts, lead schema, templates, and internal AI workflow assets. |
| `GEMINI.md` | Shared operating rules for Gemini CLI and Antigravity CLI. |
| `.agents/agents/acting-automation-operator/agent.md` | Workspace-specific Antigravity agent for safe internal review and maintenance. |
| `.gemini/commands/acting/` | Reusable Gemini CLI internal status and planning commands. |
| `JULES_DAILY_MAINTENANCE_PROMPT.md` | Repository-local daily maintenance prompt for Google Jules after repository connection. |
| `CLI_AND_JULES_AUTOMATION_MANIFEST.md` | Current cross-tool roles, daily sequence, and mandatory no-outbound boundary. |

The active recurring casting workflow remains the separate research and shortlist-maintenance process. Do not create duplicate public-source research schedules in GitHub, Jules, Antigravity, or Gemini CLI.

## Important Behavior Rules

*   **No Auto-Closing Issues:** The `.github/workflows/reply_processor.yml` workflow will *never* close issues. It only applies labels and facilitates project board movement.
*   **No Auto-Messaging:** All email/DM drafts are pasted into GitHub Issues for manual review and sending. There is no automatic sending of messages.
*   **Scam Red-Flags:** `scripts/parse_leads.py` includes checks for potential scam indicators (e.g., requesting fees, using generic email domains, missing project names) and will add a `warning` label to the issue if detected.

This toolkit aims to provide a safe, transparent, and auditable way to manage your acting career outreach using familiar GitHub tools.
