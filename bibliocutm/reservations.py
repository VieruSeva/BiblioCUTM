"""Rezervări, anulări și expirări."""
from datetime import timedelta
from .models import Reservation
from .settings import RESERVATION_HOURS

def expire(library, now):
    for r in library.reservations.values():
        if r.status == 'active' and now >= r.expires_at:
            r.status = 'expired'
            library.books[r.inventory_id].status = 'available'

def reserve(library, reader_id, inventory_id, now):
    expire(library, now)
    library.eligible(reader_id, now)
    book = library.books[inventory_id]
    if book.status != 'available':
        raise ValueError('Exemplarul nu este disponibil')
    rid = f'R{len(library.reservations) + 1:03}'
    r = Reservation(rid, reader_id, inventory_id, now + timedelta(hours=RESERVATION_HOURS))
    library.reservations[rid] = r
    book.status = 'reserved'
    return r

def cancel(library, reader_id, reservation_id):
    r = library.reservations[reservation_id]
    if r.reader_id != reader_id:
        raise PermissionError('Rezervarea aparține altui cititor')
    if r.status == 'active':
        r.status = 'cancelled'
        library.books[r.inventory_id].status = 'available'
        return True
    return False
