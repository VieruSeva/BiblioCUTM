import unittest
from bibliocutm.models import Library, Book
from bibliocutm.catalog import add_book, search


class CatalogValidationTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        add_book(self.library, Book("B1", "Algoritmi", "Autor unu", "IT"))
        add_book(self.library, Book("B2", "Rețele", "Autor doi", "IT", "borrowed"))
        add_book(self.library, Book("B3", "Algebră", "Autor trei", "Matematică"))

    def test_search_ignores_outer_spaces_and_case(self):
        results = search(self.library, "  ALGORITMI  ")
        self.assertEqual([book.inventory_id for book in results], ["B1"])

    def test_search_combines_filters(self):
        results = search(self.library, "  autor  ", category="IT", available_only=True)
        self.assertEqual([book.inventory_id for book in results], ["B1"])

    def test_whitespace_query_preserves_category_and_availability(self):
        results = search(self.library, "   ", category="IT", available_only=True)
        self.assertEqual([book.inventory_id for book in results], ["B1"])

    def test_required_fields_reject_empty_or_whitespace(self):
        initial = dict(self.library.books)
        for field in ("inventory_id", "title", "author", "category"):
            for value in ("", "   ", None):
                with self.subTest(field=field, value=value):
                    data = dict(inventory_id="B4", title="Carte", author="Autor", category="IT")
                    data[field] = value
                    with self.assertRaisesRegex(ValueError, field):
                        add_book(self.library, Book(**data))
                    self.assertEqual(self.library.books, initial)

    def test_duplicate_inventory_keeps_original(self):
        original = self.library.books["B1"]
        with self.assertRaises(ValueError):
            add_book(self.library, Book("B1", "Alt titlu", "Alt autor", "IT"))
        self.assertIs(self.library.books["B1"], original)

    def test_validation_does_not_mutate_valid_input(self):
        book = Book("B4", " Titlu cu spații ", " Autor ", "IT")
        add_book(self.library, book)
        search(self.library, " titlu ")
        self.assertEqual(book.title, " Titlu cu spații ")
        self.assertEqual(book.author, " Autor ")


if __name__ == "__main__":
    unittest.main()
