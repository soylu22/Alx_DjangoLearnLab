from bookshelf.models import Book

books = Book.objects.all()
print(books)

# Expected output:
# <QuerySet [<Book: 1984>]>

# Retrieve a single book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

# Expected output:
# 1984 George Orwell 1949
