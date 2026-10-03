import sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts'))
from daily_job import run
from init import connect

class TokenBudgetTests(unittest.TestCase):
    def test_daily_job_is_idempotent(self):
        db=Path(tempfile.mkdtemp())/'memory.db'
        payload={'daily_log':{'date':'2026-10-04','summary':'讨论职业方向。','events':[],'emotions':[],'topics':['职业']},'memory_updates':[{'content':'用户明确想创业','type':'goal','importance':3}]}
        run(db,payload); run(db,payload)
        con=connect(db)
        self.assertEqual(con.execute('SELECT COUNT(*) FROM daily_logs').fetchone()[0],1)
        self.assertEqual(con.execute("SELECT mention_count FROM memories WHERE content='用户明确想创业'").fetchone()[0],2)
        con.close()
