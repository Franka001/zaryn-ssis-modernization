import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from pipeline import load

SOURCE = Path(__file__).resolve().parent / "data/sample/changes.csv"

class ModernizationTests(unittest.TestCase):
    def test_reconciliation_and_rerun(self):
        with TemporaryDirectory() as folder:
            db = Path(folder) / "demo.db"
            first = load(SOURCE, db)
            self.assertEqual(first["row_count"], 2)
            self.assertEqual(first["total_amount_cents"], 17000)
            self.assertEqual(first["checkpoint"], 5)
            self.assertEqual(load(SOURCE, db)["applied_events"], 0)

    def test_incremental_update_and_delete(self):
        with TemporaryDirectory() as folder:
            source, db = Path(folder) / "initial.csv", Path(folder) / "demo.db"
            source.write_text("\n".join(SOURCE.read_text().splitlines()[:3]) + "\n")
            self.assertEqual(load(source, db)["row_count"], 2)
            self.assertEqual(load(SOURCE, db)["applied_events"], 3)
            with sqlite3.connect(db) as conn:
                self.assertEqual(dict(conn.execute("SELECT * FROM orders")), {"O100": 12000, "O300": 5000})

    def test_failure_rolls_back(self):
        with TemporaryDirectory() as folder:
            db = Path(folder) / "demo.db"
            with self.assertRaises(RuntimeError):
                load(SOURCE, db, fail_after=2)
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 0)
                self.assertEqual(conn.execute("SELECT seq FROM checkpoint").fetchone()[0], 0)
            self.assertTrue(load(SOURCE, db)["reconciled"])

    def test_duplicate_sequence_rejected(self):
        with TemporaryDirectory() as folder:
            source = Path(folder) / "bad.csv"
            source.write_text(SOURCE.read_text() + "5,O400,U,100\n")
            with self.assertRaises(ValueError):
                load(source, Path(folder) / "demo.db")

if __name__ == "__main__":
    unittest.main()
