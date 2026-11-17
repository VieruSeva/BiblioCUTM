import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bibliocutm.models import Library, Reader, Book
from bibliocutm.catalog import add_book
from bibliocutm.loans import issue, return_book
from bibliocutm.reports import reader_history


class ReaderHistoryTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.now = datetime(2026, 11, 17, 10, tzinfo=ZoneInfo("Europe/Chisinau"))
        for reader_id in ("r1", "r2"):
            self.library.readers[reader_id] = Reader(reader_id)
        for number in range(1, 5):
            add_book(self.library, Book(f"B{number}", f"Carte {number}", "Autor", "IT"))

    def test_history_is_isolated_by_reader(self):
        own = issue(self.library, "r1", "B1", self.now)
        issue(self.library, "r2", "B2", self.now)
        self.assertEqual(reader_history(self.library, "r1"), [own])

    def test_history_includes_returned_loans(self):
        loan = issue(self.library, "r1", "B1", self.now)
        return_book(self.library, loan.loan_id, self.now + timedelta(hours=1))
        self.assertEqual(reader_history(self.library, "r1"), [loan])
        self.assertIsNotNone(reader_history(self.library, "r1")[0].returned_at)

    def test_history_sorts_without_mutating_storage(self):
        later = issue(self.library, "r1", "B1", self.now + timedelta(hours=1))
        earlier = issue(self.library, "r1", "B2", self.now)
        self.assertEqual(reader_history(self.library, "r1"), [earlier, later])
        self.assertEqual(list(self.library.loans), [later.loan_id, earlier.loan_id])

    def test_empty_history(self):
        self.assertEqual(reader_history(self.library, "r1"), [])

    def test_unknown_reader(self):
        with self.assertRaisesRegex(ValueError, "Cititorul nu există"):
            reader_history(self.library, "missing")


if __name__ == "__main__":
    unittest.main()
