#!/usr/bin/env python3
"""Soft-delete one exact memory; deleted records are retained only for audit/export."""
import argparse, json
from pathlib import Path
from init import DEFAULT_DB, connect, initialize

def forget(db, memory_id):
    initialize(db); con=connect(db)
    cursor=con.execute("UPDATE memories SET status='deleted', updated_at=CURRENT_TIMESTAMP WHERE id=? AND status='active'", (memory_id,))
    con.commit(); con.close(); return cursor.rowcount
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('memory_id',type=int); p.add_argument('--db',type=Path,default=DEFAULT_DB); a=p.parse_args()
    print(json.dumps({'deleted': forget(a.db,a.memory_id)}))
