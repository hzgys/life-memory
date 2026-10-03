# Life Memory MVP

Private local-memory MVP for compact daily records and long-term review. It uses Python’s standard-library SQLite driver; no cloud service or vector database is required.

```bash
python3 scripts/init.py
python3 scripts/ingest.py "用户决定未来转向 AI 方向" --type career --importance 3 --tags AI,职业
python3 scripts/retrieve.py "职业 AI"
python3 scripts/forget.py 1
python3 scripts/export.py life-memory-export.json
python3 -m unittest discover -s tests -v
```

`daily_job.py` accepts a path to a structured daily-processor JSON result. It upserts the date, so it is safe to retry. The database is stored at `data/life_memory.db` unless `--db` supplies a different private path.

Memory values: `0` ignore, `1` daily-only, `2` long-lived memory, `3` durable decision/goal. Deleted memories stay in the export for auditability but are excluded from retrieval.
