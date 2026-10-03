#!/usr/bin/env python3
"""Idempotently persist an LLM-produced daily JSON payload."""
import argparse, json
from pathlib import Path
from init import DEFAULT_DB, connect, initialize
from ingest import add_memory

def estimate(value): return len(json.dumps(value, ensure_ascii=False)) // 4
def run(db, payload):
    daily=payload['daily_log']; day=daily['date']; initialize(db)
    con=connect(db)
    con.execute("INSERT INTO daily_logs(date,summary,events_json,emotions_json,topics_json,memory_candidates_json,token_estimate) VALUES(?,?,?,?,?,?,?) ON CONFLICT(date) DO UPDATE SET summary=excluded.summary, events_json=excluded.events_json, emotions_json=excluded.emotions_json, topics_json=excluded.topics_json, memory_candidates_json=excluded.memory_candidates_json, token_estimate=excluded.token_estimate", (day,daily.get('summary',''),json.dumps(daily.get('events',[]),ensure_ascii=False),json.dumps(daily.get('emotions',[]),ensure_ascii=False),json.dumps(daily.get('topics',[]),ensure_ascii=False),json.dumps(payload.get('memory_updates',[]),ensure_ascii=False),estimate(daily)))
    con.commit(); con.close(); updates=[]
    for candidate in payload.get('memory_updates',[]):
        if candidate.get('importance', 0) >= 2:
            updates.append(add_memory(db, candidate['content'], candidate.get('type','experience'), candidate['importance'], candidate.get('confidence',1.0), day, candidate.get('tags', daily.get('topics',[]))))
    return {"date":day,"memory_updates":updates}
if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('payload',type=Path); p.add_argument('--db',type=Path,default=DEFAULT_DB); a=p.parse_args()
    print(json.dumps(run(a.db,json.loads(a.payload.read_text())),ensure_ascii=False))
