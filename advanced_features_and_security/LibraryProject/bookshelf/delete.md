from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

books = Book.objects.all()
print(books)

# Expected output:
# <QuerySet []>   (empty, since the book was deleted)
