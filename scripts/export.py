#!/usr/bin/env python3
"""Export every table as a portable JSON document."""
import argparse, json
from pathlib import Path
from init import DEFAULT_DB, connect, initialize
def export(db, output):
    initialize(db); con=connect(db); result={}
    for table in ('conversations','daily_logs','memories','tags','memory_tags','patterns'):
        result[table]=[dict(row) for row in con.execute(f'SELECT * FROM {table}')]
    con.close(); output.write_text(json.dumps(result,ensure_ascii=False,indent=2)); return output
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('output',type=Path); p.add_argument('--db',type=Path,default=DEFAULT_DB); a=p.parse_args(); print(export(a.db,a.output))
