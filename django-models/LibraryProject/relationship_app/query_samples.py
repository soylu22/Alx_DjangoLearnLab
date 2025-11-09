import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Example Queries

# 1. Query all books by a specific author
author = Author.objects.first()  # get the first author
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

# 2. List all books in a library
library = Library.objects.first()  # get the first library
books_in_library = library.books.all()
print(f"Books in {library.name}: {[book.title for book in books_in_library]}")

# 3. Retrieve the librarian for a library
librarian = library.librarian
print(f"Librarian of {library.name}: {librarian.name}")
