#!/usr/bin/env python3
"""Small, deterministic retrieval over active memories and tags."""
import argparse, json
from pathlib import Path
from init import DEFAULT_DB, connect, initialize

def retrieve(db, query, limit=5, memory_type=None):
    initialize(db); limit=min(max(limit,1),10); terms=[x.casefold() for x in query.split() if len(x)>1]
    con=connect(db); where="m.status='active'"; params=[]
    if memory_type: where += " AND m.type=?"; params.append(memory_type)
    rows=con.execute(f"SELECT DISTINCT m.* FROM memories m LEFT JOIN memory_tags mt ON mt.memory_id=m.id LEFT JOIN tags t ON t.id=mt.tag_id WHERE {where} ORDER BY m.importance DESC, m.last_seen DESC",params).fetchall(); con.close()
    def score(row):
        hay=(row['content']+' '+row['type']).casefold(); return sum(term in hay for term in terms)*10 + row['importance'] + min(row['mention_count'],5)/10
    selected=sorted(rows,key=score,reverse=True)
    if terms: selected=[row for row in selected if score(row)>row['importance']]
    selected=selected[:limit]
    return {"memories":[dict(row) for row in selected],"confidence": round(0.9 if selected else 0.0,2),"context_estimate":sum(len(row['content'])//4 for row in selected)}
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('query'); p.add_argument('--db',type=Path,default=DEFAULT_DB); p.add_argument('--limit',type=int,default=5); p.add_argument('--type'); a=p.parse_args(); print(json.dumps(retrieve(a.db,a.query,a.limit,a.type),ensure_ascii=False))
