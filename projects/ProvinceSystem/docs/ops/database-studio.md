# Database studio

Owners (website role `root`) browse, query and edit the site's databases at
**Staff panel → Database** (`/admin/database`). The tab only shows for roles with
the `use_database` capability, which is root only. Code:
[`backend/src/dbstudio/studio.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/dbstudio/studio.py),
[`backend/src/api/database_routes.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/database_routes.py)
and `frontend/app/components/admin/database/`.

## Databases

Each site lists the databases it can reach:

| Id | What | Access |
|----|------|--------|
| `site` | `province.db`: accounts, characters, wardrobes, chronicle and ledger indexes, the staff audit log | Read and edit |
| `coreprotect` | The CoreProtect SQLite file named by `COREPROTECT_DB` (Main on www, Dev on the Dev site) | Read only |
| `postgres` | The site's Postgres in `DATABASE_URL` (Precedent and patch notes), `public` schema | Read and edit |

The list shows each database's tables, size and how many audited queries it has had.
Opening one shows its tables with columns and approximate row counts (`max(rowid)` on
SQLite, `reltuples` on Postgres), query tabs and table tabs. Query tabs are kept in
the browser's local storage per database.

## Reading

Every query is one statement, enforced by the databases themselves: Python's
`sqlite3` refuses a second statement, and Postgres statements go through the extended
protocol (psycopg 3), which refuses several commands. As a second layer with clearer
messages, the studio also refuses before connecting transaction and session control (`BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET`, `RESET`, `DISCARD`,
…), `VACUUM`, `ATTACH`, `DETACH` and `COPY`; semicolons inside strings, quoted names,
dollar quotes and comments are ignored when counting statements.

Reads run on connections that cannot write: SQLite opened with `mode=ro` and
`PRAGMA query_only`, Postgres in a read-only transaction through a server-side cursor
(`DECLARE … CURSOR FOR`),
so a Postgres read must be a query (`SELECT`, `WITH`, `VALUES`, `TABLE`) and its rows
arrive as they are fetched. Each statement returns at most 1,000 rows and stops after
10 seconds on the site and Postgres databases. SQLite reads may call schema pragmas
such as `table_info`; pragmas that change settings are refused.

CoreProtect reads go through the same guarded reader as the CoreProtect pages
([coreprotect.md](../integrations/coreprotect.md)): one reader at a time and a
3-second budget, because a long read holds off CoreProtect's writes. Filter on
indexed columns (`user`, `time`, `wid`, `x`/`z`) and add a `LIMIT`.

A table tab pages through `SELECT * FROM <table>` with an optional `WHERE` filter
and sorting by any column; **Open as query** copies the statement into a query tab.
One click on a table opens it in a reused preview tab (italic title); a double click,
or paging, sorting or filtering in it, keeps the tab open.

CSV exports prefix text that starts with `=`, `+`, `-`, `@`, a tab or a carriage
return with `'`, so player-written text cannot run as a spreadsheet formula.

Text values in columns whose names look secret (`token`, `secret`, `password`,
`nonce`, `api_key`, such as `token_hash` and `refresh_token`) show as `••••••`.
This keeps them off the screen; it is not access control. Integers beyond 2^53 are
sent as text, and blobs as their size and first 32 bytes in hex.

## Editing

On a writable database, switch a query tab from **Read** to **Edit**. The studio
shows the statement and asks before running it. Edits run in one transaction with
foreign keys on (SQLite) and the same time limits, and the result shows the rows
changed. The audit log table `admin_audit` cannot be changed, dropped or have its
triggers or indexes changed from the studio, and `sqlite_sequence` (which holds its
ID counter) cannot be written. Triggers cannot be created on the site database at
all, because a stored trigger would later run outside the studio's checks, and
`PRAGMA writable_schema` and other setting changes are refused.

## Audit

Every browse, query and edit is written to the staff audit log as
`database.read` or `database.write`, with the database, the statement (first 2,000
characters), the outcome and the row counts. An edit is logged as `requested` before
it runs, so if the audit log cannot be written the edit does not happen. Opening the
list (`database.list`) and a database's tables (`database.schema`) are logged too.
The list's query count covers reads and edits with an outcome.

## Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/admin/database` | GET | Databases with tables, size and query counts |
| `/admin/database/{id}/schema` | GET | Tables, views and columns |
| `/admin/database/{id}/browse` | POST | One page of a table: `table`, `offset`, `limit` (≤ 500), `order`, `descending`, `where` |
| `/admin/database/{id}/query` | POST | Run `sql`; `write: true` for an edit |

All need a root session; the POST routes also need the site's `Origin`. SQL errors
come back as **400** with the database's message, timeouts as **408**, a busy
CoreProtect reader as **409** and refused statements as **403**.
