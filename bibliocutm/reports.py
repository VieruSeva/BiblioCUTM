"""Exportul împrumuturilor active în format CSV."""
import csv
import io

def active_loans_csv(library, now):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream)
    writer.writerow(['loan_id', 'reader_id', 'inventory_id', 'due_at', 'overdue'])
    for loan in library.loans.values():
        if loan.returned_at is None:
            writer.writerow([loan.loan_id, loan.reader_id, loan.inventory_id,
                             loan.due_at.isoformat(), now > loan.due_at])
    return stream.getvalue()


def reader_history(library, reader_id):
    if reader_id not in library.readers:
        raise ValueError("Cititorul nu există")
    return sorted(
        (loan for loan in library.loans.values() if loan.reader_id == reader_id),
        key=lambda loan: (loan.issued_at, loan.loan_id),
    )
