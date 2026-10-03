#!/usr/bin/env python3
"""Initialize the local Life Memory SQLite database."""
import argparse
import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parents[1] / "data" / "life_memory.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
 id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, content TEXT NOT NULL,
 source TEXT, importance INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS daily_logs (
 date TEXT PRIMARY KEY, summary TEXT NOT NULL, events_json TEXT, emotions_json TEXT,
 topics_json TEXT, memory_candidates_json TEXT, token_estimate INTEGER DEFAULT 0,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS memories (
 id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL, content TEXT NOT NULL,
 confidence REAL DEFAULT 1.0, importance INTEGER DEFAULT 2, first_seen TEXT, last_seen TEXT,
 mention_count INTEGER DEFAULT 1, status TEXT DEFAULT 'active', source_date TEXT,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS memory_tags (memory_id INTEGER, tag_id INTEGER,
 PRIMARY KEY(memory_id, tag_id), FOREIGN KEY(memory_id) REFERENCES memories(id), FOREIGN KEY(tag_id) REFERENCES tags(id));
CREATE TABLE IF NOT EXISTS patterns (
 id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, evidence_count INTEGER DEFAULT 0,
 confidence REAL DEFAULT 0.5, first_seen TEXT, last_seen TEXT, status TEXT DEFAULT 'observing',
 created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE INDEX IF NOT EXISTS idx_memories_active ON memories(status, type, last_seen);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
"""

def connect(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize(path):
    connection = connect(path)
    connection.executescript(SCHEMA)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = parser.parse_args()
    initialize(args.db)
    print(args.db)
