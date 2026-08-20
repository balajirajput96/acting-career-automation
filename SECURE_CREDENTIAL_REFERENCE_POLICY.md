# Secure Credential Reference Policy

## Purpose

This repository preserves **automation references**, not credential material. It may document which approved integration a workflow uses and how to verify that an official login is present, but it never stores API keys, OAuth tokens, passwords, session cookies, private keys, recovery codes, or credential exports.

## Approved Persistence Model

| Integration Type | Safe Persistence Location | Repository Rule |
|---|---|---|
| GitHub workflows | GitHub Actions secret or environment configuration | Reference the secret name only when a workflow genuinely needs it; never commit a value. |
| Official CLI login | The CLI’s official local credential store | Record the CLI name, version, safe readiness check, and account context only. |
| Browser-connected account | Browser session or supported connector authorization | Record that a connection is required or verified, never session data. |
| Google Workspace / connectors | Approved connector authorization store | Record the permitted task and verification result, never an API key or OAuth payload. |
| Local development environment | Local `.env` or other ignored secret file | Keep outside version control and never include it in an artifact, log, or documentation file. |

## Required Rules

1. Do not extract, print, copy, decode, transmit, or commit credential values from any environment, history file, configuration file, browser session, API response, CLI store, or connector.
2. Do not bypass authentication, MFA, authorization scopes, repository protections, account restrictions, payment gates, rate limits, or platform security controls.
3. Keep reusable automation in scripts, workflows, policy documents, run records, and tests. Keep credentials in the service’s official secure storage mechanism.
4. When a login expires, record the affected integration and request an official reauthentication flow. Do not attempt credential recovery or reverse engineering.
5. Before every commit, check the staged diff for accidental secret files or values. If exposure is suspected, stop the publish, remove the material, rotate or revoke it through the official service where appropriate, then validate again.

## Safe Historical Preservation

Terminal history and CLI state can provide useful procedural evidence, but may contain unrelated commands or secrets. Preserve only sanitized reusable procedures: command purpose, script path, validation command, failure category, and outcome. Do not copy raw history into GitHub.

## Daily Maintenance Contract

The daily maintenance layer validates repository-local scripts, schedule definitions, policy documents, and machine-readable run records. It does not authenticate by scraping browser sessions, collecting secret values, or writing credentials into GitHub.

> A successful configuration file check is not proof of authorization. Use a safe, read-only service or CLI readiness check where supported, and record only the result.
