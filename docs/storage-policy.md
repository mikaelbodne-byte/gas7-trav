# Gas7 storage policy

## Google Drive: durable archive
Keep raw ATG race/start history, compressed archival objects, verified manifests, full backups, sealed forecasts, and human-facing documents in the Gas7 data archive.

## Supabase: operational engine
Keep only data needed for current calculations and efficient lookups. Supabase Storage may be used as a transfer/staging layer, **not** the only backup copy.

## GitHub: source code
Keep application code, test fixtures with synthetic data, SQL migration scripts, documentation, and CI definitions. Never store real data dumps or tokens.

## Archive release gate
Data may be purged from operational tables only after:
1. The archive contains all expected rows and fields.
2. Every file passes read-back SHA-256 checks.
3. An independent Google Drive copy is verified.
4. A sample (or full) restore into an isolated database succeeds.
5. Foreign keys, dependencies, and retention requirements have been assessed.
6. Production is healthy with enough spare disk space.

A logical DELETE is not proof of reclaimed physical disk space.
