import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple

DB_PATH = Path("infoTable.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS infoTable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT,
                dateAdded TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """
        )


def insert_rows(quals: str | Iterable[str]) -> int:
    if isinstance(quals, str):
        quals = [quals]
    rows = [(q.strip(),) for q in quals if str(q).strip()]
    if not rows:
        return 0
    with _connect() as conn:
        cur = conn.executemany(
            "INSERT INTO infoTable(text) VALUES (?) ON CONFLICT(text) DO NOTHING",
            rows,
        )
        return cur.rowcount  # SQLite 3.24+ gives >=0; may be -1 on some builds


def replace_all(quals: Iterable[str]) -> int:
    rows = [(q.strip(),) for q in quals if str(q).strip()]
    with _connect() as conn:
        conn.execute("DELETE FROM infoTable")
        conn.execute("DELETE FROM sqlite_sequence WHERE name='infoTable'")
        if not rows:
            return 0
        cur = conn.executemany("INSERT INTO infoTable(text) VALUES (?)", rows)
        return cur.rowcount


def get_table(just_text: bool = False) -> List[str] | List[Tuple[str, str]]:
    with _connect() as conn:
        if just_text:
            return [
                r["text"]
                for r in conn.execute("SELECT text FROM infoTable ORDER BY id")
            ]
        else:
            return [
                (r["text"], r["dateAdded"])
                for r in conn.execute(
                    "SELECT text, dateAdded FROM infoTable ORDER BY id"
                )
            ]


if __name__ == "__main__":
    init_db()
