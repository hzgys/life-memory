import sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts'))
from ingest import add_memory
from retrieve import retrieve
from forget import forget

class MemoryTests(unittest.TestCase):
    def setUp(self): self.db=Path(tempfile.mkdtemp())/'memory.db'
    def test_duplicate_merges_and_deleted_memory_is_hidden(self):
        first=add_memory(self.db,'用户喜欢攀岩','preference',2,1.0,'2026-10-01',['运动'])
        second=add_memory(self.db,'用户喜欢攀岩','preference',2,1.0,'2026-10-04',['运动'])
        self.assertEqual(first['id'],second['id']); self.assertEqual(second['action'],'merged')
        self.assertEqual(retrieve(self.db,'攀岩')['memories'][0]['mention_count'],2)
        self.assertEqual(forget(self.db,first['id']),1)
        self.assertEqual(retrieve(self.db,'攀岩')['memories'],[])
    def test_changed_preference_is_preserved(self):
        add_memory(self.db,'用户希望从事项目管理','career',2,1,'2025-01-01')
        add_memory(self.db,'用户不希望长期从事项目管理','career',3,1,'2026-01-01')
        self.assertEqual(len(retrieve(self.db,'项目管理')['memories']),2)
