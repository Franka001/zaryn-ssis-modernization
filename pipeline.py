"""Local SQLite change-log demo; not an SSIS or SQL Server runtime."""
import argparse
import csv
import json
import sqlite3
from pathlib import Path


def read_events(source):
    with Path(source).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    events = []
    for row in rows:
        seq, cents = int(row["change_seq"]), int(row["amount_cents"])
        if not row["order_id"] or row["operation"] not in ("U", "D") or cents < 0:
            raise ValueError("Invalid change event")
        events.append((seq, row["order_id"], row["operation"], cents))
    events.sort()
    if [e[0] for e in events] != list(range(1, len(events) + 1)):
        raise ValueError("Supply complete contiguous history starting at sequence 1")
    return events


def load(source, database, fail_after=None):
    events = read_events(source)
    expected = {}
    for seq, key, operation, cents in events:
        if operation == "D":
            expected.pop(key, None)
        else:
            expected[key] = cents
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database)
    try:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS orders(order_id TEXT PRIMARY KEY, amount_cents INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS checkpoint(id INTEGER PRIMARY KEY CHECK(id=1), seq INTEGER NOT NULL);
        INSERT OR IGNORE INTO checkpoint VALUES(1, 0);
        """)
        with connection:
            checkpoint = connection.execute("SELECT seq FROM checkpoint WHERE id=1").fetchone()[0]
            if checkpoint > len(events):
                raise ValueError("Source history is shorter than the committed checkpoint")
            applied = 0
            for seq, key, operation, cents in events:
                if seq <= checkpoint:
                    continue
                if operation == "D":
                    connection.execute("DELETE FROM orders WHERE order_id=?", (key,))
                else:
                    connection.execute("""INSERT INTO orders VALUES(?, ?)
                        ON CONFLICT(order_id) DO UPDATE SET amount_cents=excluded.amount_cents""", (key, cents))
                applied += 1
                if fail_after is not None and applied >= fail_after:
                    raise RuntimeError("Injected failure before checkpoint commit")
            actual = dict(connection.execute("SELECT order_id, amount_cents FROM orders"))
            if actual != expected:
                raise ValueError("Reconciliation failed; transaction will roll back")
            connection.execute("UPDATE checkpoint SET seq=? WHERE id=1", (len(events),))
        return dict(applied_events=applied, checkpoint=len(events), row_count=len(actual),
                    total_amount_cents=sum(actual.values()), reconciled=True)
    finally:
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data/sample/changes.csv")
    parser.add_argument("--database", default="output/demo.db")
    args = parser.parse_args()
    print(json.dumps(load(args.source, args.database), indent=2))
