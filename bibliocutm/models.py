"""Modele de date în memorie pentru demonstrația Git."""
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Book:
    inventory_id: str
    title: str
    author: str
    category: str
    status: str = 'available'

@dataclass
class Reader:
    reader_id: str
    active: bool = True

@dataclass
class Reservation:
    reservation_id: str
    reader_id: str
    inventory_id: str
    expires_at: datetime
    status: str = 'active'

@dataclass
class Loan:
    loan_id: str
    reader_id: str
    inventory_id: str
    issued_at: datetime
    due_at: datetime
    returned_at: datetime | None = None

@dataclass
class Library:
    books: dict[str, Book] = field(default_factory=dict)
    readers: dict[str, Reader] = field(default_factory=dict)
    reservations: dict[str, Reservation] = field(default_factory=dict)
    loans: dict[str, Loan] = field(default_factory=dict)

    def engagements(self, reader_id, now):
        reservations = sum(r.reader_id == reader_id and r.status == 'active'
                           and now < r.expires_at for r in self.reservations.values())
        loans = sum(l.reader_id == reader_id and l.returned_at is None
                    for l in self.loans.values())
        return reservations + loans

    def eligible(self, reader_id, now, additional=True):
        reader = self.readers.get(reader_id)
        if reader is None or not reader.active:
            raise ValueError('Contul cititorului este inactiv sau inexistent')
        if any(l.reader_id == reader_id and l.returned_at is None and now > l.due_at
               for l in self.loans.values()):
            raise ValueError('Există un împrumut întârziat')
        from .settings import MAX_ENGAGEMENTS
        if self.engagements(reader_id, now) + int(additional) > MAX_ENGAGEMENTS:
            raise ValueError('Limita de exemplare angajate este depășită')
