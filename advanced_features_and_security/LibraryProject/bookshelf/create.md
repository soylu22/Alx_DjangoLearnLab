from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Expected output:
# A new Book instance is created successfully.
# Example: <Book: 1984>
