# Gas7 Trav

Development repository for Gas7's horse-racing analysis engine.

> **Status:** Initial non-sensitive project skeleton. No production code or datasets have been migrated.

## Architecture

| Component | Responsibility |
| --- | --- |
| Google Drive | Source-data archives, sealed forecasts, backups and documentation |
| Supabase | Operational PostgreSQL database, processing, jobs and analytical calculations |
| GitHub | Versioned source code, tests, documentation and deployment configuration |
| Vercel | Optional application UI |

## Safety rules

- **Never commit** ATG raw data, personal information, database dumps, credentials or API tokens.
- Archive source data independently in Google Drive and verify its checksums before any deletion.
- Do not run destructive SQL migrations or `VACUUM FULL` against production during disk incidents.
- Do not automatically deploy or run migrations from this repository.
- New code is developed in branches and reviewed before production use.

## Current operations

The project has experienced a PostgreSQL disk-full outage. Recovery is tracked separately; this repository is **not** a database backup.

See [the recovery runbook](docs/recovery-runbook.md).
