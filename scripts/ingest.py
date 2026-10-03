#!/usr/bin/env python3
"""Add a compressed conversation event or a durable memory."""
import argparse, json, re
from datetime import date, datetime, timezone
from pathlib import Path
from init import DEFAULT_DB, connect, initialize

ALLOWED_TYPES = {"fact", "preference", "goal", "decision", "relationship", "experience", "value", "career", "habit", "belief", "pattern"}
def norm(value): return re.sub(r"\s+", " ", value.strip().casefold())
def today(): return date.today().isoformat()

def add_memory(db, content, memory_type, importance, confidence, source_date, tags=()):
    if memory_type not in ALLOWED_TYPES: raise ValueError("unsupported memory type")
    initialize(db); con = connect(db); key = norm(content)
    row = con.execute("SELECT id, mention_count FROM memories WHERE status='active' AND type=? AND lower(trim(content))=?", (memory_type, key)).fetchone()
    if row:
        con.execute("UPDATE memories SET mention_count=?, last_seen=?, confidence=MAX(confidence, ?), importance=MAX(importance, ?), updated_at=CURRENT_TIMESTAMP WHERE id=?", (row['mention_count']+1, source_date, confidence, importance, row['id']))
        memory_id, action = row['id'], "merged"
    else:
        cursor = con.execute("INSERT INTO memories(type, content, confidence, importance, first_seen, last_seen, source_date) VALUES(?,?,?,?,?,?,?)", (memory_type, content.strip(), confidence, importance, source_date, source_date, source_date))
        memory_id, action = cursor.lastrowid, "created"
    for tag in {norm(tag) for tag in tags if tag.strip()}:
        con.execute("INSERT OR IGNORE INTO tags(name) VALUES(?)", (tag,))
        tag_id = con.execute("SELECT id FROM tags WHERE name=?", (tag,)).fetchone()['id']
        con.execute("INSERT OR IGNORE INTO memory_tags(memory_id, tag_id) VALUES(?,?)", (memory_id, tag_id))
    con.commit(); con.close(); return {"id": memory_id, "action": action}

if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("content"); parser.add_argument("--db", type=Path, default=DEFAULT_DB); parser.add_argument("--type", default="experience"); parser.add_argument("--importance", type=int, default=2); parser.add_argument("--confidence", type=float, default=1.0); parser.add_argument("--date", default=today()); parser.add_argument("--tags", default=""); parser.add_argument("--conversation", action="store_true")
    a=parser.parse_args(); initialize(a.db)
    if a.conversation:
        con=connect(a.db); con.execute("INSERT INTO conversations(timestamp,content,source,importance) VALUES(?,?,?,?)", (datetime.now(timezone.utc).isoformat(), a.content, "manual", a.importance)); con.commit(); con.close(); print(json.dumps({"action":"conversation_saved"}))
    else: print(json.dumps(add_memory(a.db,a.content,a.type,a.importance,a.confidence,a.date,a.tags.split(',')), ensure_ascii=False))
