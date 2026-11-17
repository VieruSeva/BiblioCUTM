"""Operații asupra catalogului."""
def search(library, query='', category=None, available_only=False):
    query = query.strip().casefold()
    return [b for b in library.books.values()
            if (query in b.title.casefold() or query in b.author.casefold())
            and (category is None or b.category == category)
            and (not available_only or b.status == 'available')]

def add_book(library, book):
    for field in ("inventory_id", "title", "author", "category"):
        value = getattr(book, field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Câmpul {field} este obligatoriu")
    if book.inventory_id in library.books:
        raise ValueError('Numărul de inventar există deja')
    library.books[book.inventory_id] = book
