# SECURITY.md — Minimum Security Requirements

## Secrets

- provider API keys only on server side;
- use environment/secret manager;
- never commit `.env` containing real secrets;
- redact secrets in logs.

## Uploads

- allowlist MIME types;
- maximum file size;
- image dimension limits;
- reject malformed files;
- isolate processing where possible.

## Sessions

A user may access only their own session data.

## AI prompts

Treat uploaded text/images as untrusted input.
Do not let user content override system/security policies.

## Logs

Do not log raw secrets.
Minimize sensitive student data in telemetry.

## Third-party providers

Keep provider-specific credentials/config isolated from user-visible code.

## Production later

Add stronger authentication, audit logging, encryption policies, rate limiting per user, and backup/retention policies before exposing the system broadly.
