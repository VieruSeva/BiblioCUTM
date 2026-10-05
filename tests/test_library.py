import csv
import io
import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bibliocutm.models import Library, Reader, Book
from bibliocutm.catalog import add_book, search
from bibliocutm.reservations import reserve, cancel, expire
from bibliocutm.loans import issue, return_book
from bibliocutm.reports import active_loans_csv
from bibliocutm.roles import require_permission

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.lib = Library()
        self.now = datetime(2026, 10, 5, 12, 0, tzinfo=ZoneInfo('Europe/Chisinau'))
        for rid in ('r1', 'r2'):
            self.lib.readers[rid] = Reader(rid)
        for n in range(1, 5):
            add_book(self.lib, Book(f'B{n}', f'Algoritmi {n}', 'Autor demo', 'IT'))

    def test_search_and_duplicate_inventory(self):
        self.assertEqual(len(search(self.lib, 'ALGORITMI', 'IT')), 4)
        self.assertEqual(search(self.lib, 'inexistent'), [])
        with self.assertRaises(ValueError):
            add_book(self.lib, Book('B1', 'Duplicate', 'Demo', 'IT'))

    def test_cannot_reserve_same_copy_twice(self):
        reserve(self.lib, 'r1', 'B1', self.now)
        with self.assertRaises(ValueError):
            reserve(self.lib, 'r2', 'B1', self.now)
        self.assertEqual(len(self.lib.reservations), 1)

    def test_maximum_three_engagements(self):
        for bid in ('B1', 'B2', 'B3'):
            reserve(self.lib, 'r1', bid, self.now)
        with self.assertRaises(ValueError):
            reserve(self.lib, 'r1', 'B4', self.now)

    def test_exact_expiry_boundary(self):
        r = reserve(self.lib, 'r1', 'B1', self.now)
        expire(self.lib, self.now + timedelta(hours=48, microseconds=-1))
        self.assertEqual(r.status, 'active')
        expire(self.lib, self.now + timedelta(hours=48))
        self.assertEqual(r.status, 'expired')
        self.assertEqual(self.lib.books['B1'].status, 'available')

    def test_cancel_ownership_and_repeat(self):
        r = reserve(self.lib, 'r1', 'B1', self.now)
        with self.assertRaises(PermissionError):
            cancel(self.lib, 'r2', r.reservation_id)
        self.assertTrue(cancel(self.lib, 'r1', r.reservation_id))
        self.assertFalse(cancel(self.lib, 'r1', r.reservation_id))

    def test_conversion_at_limit_and_due_date(self):
        for bid in ('B1', 'B2', 'B3'):
            reserve(self.lib, 'r1', bid, self.now)
        loan = issue(self.lib, 'r1', 'B1', self.now)
        self.assertEqual(self.lib.engagements('r1', self.now), 3)
        self.assertEqual(loan.due_at.isoformat(), '2026-10-19T23:59:59+03:00')
        self.assertEqual(self.lib.reservations['R001'].status, 'converted')

    def test_cannot_borrow_other_reader_reservation(self):
        reserve(self.lib, 'r1', 'B1', self.now)
        with self.assertRaises(ValueError):
            issue(self.lib, 'r2', 'B1', self.now)

    def test_overdue_and_disabled_reader(self):
        loan = issue(self.lib, 'r1', 'B1', self.now)
        late = loan.due_at + timedelta(seconds=1)
        with self.assertRaises(ValueError):
            reserve(self.lib, 'r1', 'B2', late)
        self.lib.readers['r1'].active = False
        self.assertTrue(return_book(self.lib, loan.loan_id, late))
        self.assertFalse(return_book(self.lib, loan.loan_id, late))
        with self.assertRaises(ValueError):
            reserve(self.lib, 'r1', 'B2', late)

    def test_csv_only_active_loans(self):
        one = issue(self.lib, 'r1', 'B1', self.now)
        two = issue(self.lib, 'r2', 'B2', self.now)
        return_book(self.lib, two.loan_id, self.now)
        rows = list(csv.DictReader(io.StringIO(active_loans_csv(self.lib, one.due_at + timedelta(seconds=1)))))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['loan_id'], one.loan_id)
        self.assertEqual(rows[0]['overdue'], 'True')

    def test_role_permissions(self):
        self.assertTrue(require_permission('librarian', 'issue'))
        with self.assertRaises(PermissionError):
            require_permission('reader', 'issue')
        with self.assertRaises(PermissionError):
            require_permission('unknown', 'search')

if __name__ == '__main__':
    unittest.main()
