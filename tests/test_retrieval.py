import sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts'))
from ingest import add_memory
from retrieve import retrieve

class RetrievalTests(unittest.TestCase):
    def test_returns_only_relevant_top_k_with_small_context(self):
        db=Path(tempfile.mkdtemp())/'memory.db'
        for n in range(8): add_memory(db,f'用户的职业目标是创业 {n}','career',3,1,'2026-10-01')
        add_memory(db,'用户喜欢看电影','preference',2,1,'2026-10-01')
        result=retrieve(db,'职业 创业',limit=5)
        self.assertEqual(len(result['memories']),5)
        self.assertTrue(all('创业' in row['content'] for row in result['memories']))
        self.assertLessEqual(result['context_estimate'],300)
