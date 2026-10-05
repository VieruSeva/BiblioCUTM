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
