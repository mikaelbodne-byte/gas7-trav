# Gas7 PostgreSQL recovery runbook

**Read-only first. Do not run this until PostgreSQL is reachable.**

## 1. Confirm infrastructure recovery

- Check Supabase project and database status.
- Confirm disk capacity has been expanded if required.
- If the database remains unavailable, contact Supabase support before attempting repair or rollback.
- Preserve the existing database and Storage objects. Do not blindly restore a snapshot.

## 2. Perform read-only checks

```sql
select now() as checked_at,
       current_setting('default_transaction_read_only') as read_only,
       pg_database_size(current_database()) as database_bytes,
       pg_postmaster_start_time() as server_started_at;
```

```sql
select schemaname, relname,
       pg_size_pretty(pg_total_relation_size(format('%I.%I', schemaname, relname)::regclass)) as total_size
from pg_stat_user_tables
order by pg_total_relation_size(format('%I.%I', schemaname, relname)::regclass) desc
limit 20;
```

## 3. Protect archived data

- Reconcile source counts against archived manifests.
- Confirm race and starter files are readable, complete, and hash verified.
- Store an independent Google Drive copy **before** deleting anything in Supabase.
- Restore into an isolated test environment before relying on archive recovery.

## 4. Re-enable operations cautiously

- Inspect scheduled jobs and ingest rates before enabling historical backfills.
- Keep bulk maintenance and `VACUUM FULL` disabled until free disk capacity is verified.
- Review monitoring thresholds for disk, WAL growth, and archive throughput.

All actions affecting production require explicit approval and an independently verified backup.
