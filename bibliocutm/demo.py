"""Demonstrație cu identificatori fictivi."""
from datetime import datetime
from zoneinfo import ZoneInfo
from .models import Library, Reader, Book
from .catalog import add_book, search
from .reservations import reserve
from .loans import issue, return_book
from .reports import active_loans_csv
from .roles import require_permission

def main():
    library = Library()
    now = datetime(2026, 10, 5, 12, 0, tzinfo=ZoneInfo('Europe/Chisinau'))
    library.readers['reader-demo'] = Reader('reader-demo')
    add_book(library, Book('BC001', 'Algoritmi', 'Autor demonstrativ', 'Informatica'))
    require_permission('reader', 'reserve')
    print('Catalog:', [b.title for b in search(library, 'alg')])
    reservation = reserve(library, 'reader-demo', 'BC001', now)
    print('Rezervare:', reservation.reservation_id, reservation.expires_at.isoformat())
    require_permission('librarian', 'issue')
    loan = issue(library, 'reader-demo', 'BC001', now)
    print('Împrumut:', loan.loan_id, loan.due_at.isoformat())
    print(active_loans_csv(library, now).strip())
    return_book(library, loan.loan_id, now)
    print('Stare după returnare:', library.books['BC001'].status)

if __name__ == '__main__':
    main()
