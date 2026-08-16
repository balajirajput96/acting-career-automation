# CLI and Jules Automation Manifest

## Purpose

This manifest keeps internal acting-career automation organized across the available tools without creating autonomous outbound communication.

| Surface | Configured role | Operating boundary |
| --- | --- | --- |
| Antigravity CLI | `acting-automation-operator` workspace agent for internal readiness checks, toolkit maintenance, factual preparation, and scam-risk review. | No external communication, publishing, payments, submissions, social posting, or fabricated claims. |
| Gemini CLI | `GEMINI.md` rules plus `/acting:status` and `/acting:plan` project commands for read-only review and safe internal planning. | No external communication, publishing, payments, submissions, or social posting. |
| GitHub Actions | Daily toolkit validation and repository-local workflow checks. | No issue or pull-request closure, and no external outreach. |
| Twice-Daily Casting Desk | Active recurring research, screening, shortlist maintenance, and factual preparation workflow. | Runs at 05:58 Asia/Kolkata; reviews at most 10 sources per run and 20 per day; no outbound actions. |
| Google Jules | Daily repository-local maintenance prompt is prepared in `JULES_DAILY_MAINTENANCE_PROMPT.md`. | Connect the repository in Jules, use a new branch or pull request, and leave merge decisions manual. |

## Daily sequence

1. GitHub Actions validates scripts, lead schema, and templates.
2. Google Jules may run the prepared repository-local maintenance prompt after the GitHub check completes.
3. The Twice-Daily Casting Desk performs public-source research and factual preparation within its documented limits.
4. Antigravity CLI and Gemini CLI are available for internal review, validation, and planning between scheduled runs.

## Mandatory boundary

No tool in this workflow may send an email, direct message, application, payment, social post, document, video, portfolio link, or other external communication. A future external submission must still have a complete truthful package and a context-specific final safeguard.

## Account-specific setup status

The Antigravity and Gemini CLI local configurations are ready. The Google Jules maintenance prompt is ready for use after the logged-in Jules session confirms access to `balajirajput96/acting-career-automation`. Other Google surfaces, including Spark, AI Studio, Drive, and Workspace, should only receive internal planning or storage tasks after their individual account pages are available.
