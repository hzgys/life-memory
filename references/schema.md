# SQLite data model

The database defaults to `data/life_memory.db`. All timestamps are ISO-8601 UTC strings; `source_date` is the user-local date when known.

- `conversations`: compressed event records; retain only user-approved or compact source data.
- `daily_logs`: one row per date, using `date` as the idempotency key.
- `memories`: facts, preferences, goals, decisions, relationships, experiences, values, careers, habits, beliefs, or patterns. `status=deleted` excludes a memory from every retrieval.
- `tags` and `memory_tags`: normalized topic tags.
- `patterns`: explicitly inferential observations, defaulting to `observing`.

The helpers retain historical memories rather than overwriting changes. A duplicate is merged only when normalized content and type match; its count and last-seen date are updated.
