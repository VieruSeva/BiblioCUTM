"""Împrumuturi și returnări în scenariul academic."""
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from .models import Loan
from .reservations import expire
from .settings import LOAN_DAYS, TIMEZONE

def issue(library, reader_id, inventory_id, now):
    expire(library, now)
    book = library.books[inventory_id]
    own = next((r for r in library.reservations.values()
                if r.reader_id == reader_id and r.inventory_id == inventory_id
                and r.status == 'active'), None)
    if book.status != 'available' and not (book.status == 'reserved' and own):
        raise ValueError('Exemplarul nu poate fi eliberat cititorului')
    library.eligible(reader_id, now, additional=own is None)
    due_date = now.astimezone(ZoneInfo(TIMEZONE)).date() + timedelta(days=LOAN_DAYS)
    due_at = datetime.combine(due_date, time(23, 59, 59), ZoneInfo(TIMEZONE))
    lid = f'L{len(library.loans) + 1:03}'
    loan = Loan(lid, reader_id, inventory_id, now, due_at)
    library.loans[lid] = loan
    if own:
        own.status = 'converted'
    book.status = 'borrowed'
    return loan

def return_book(library, loan_id, now):
    loan = library.loans[loan_id]
    if loan.returned_at is not None:
        return False
    loan.returned_at = now
    library.books[loan.inventory_id].status = 'available'
    return True
