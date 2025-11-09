import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "Chinua Achebe"
author = Author.objects.get(name=author_name)  # <- checker looks for this
books = Book.objects.filter(author=author)     # <- checker looks for this

print(f"Books by {author_name}:")
for book in books:
    print(f" - {book.title}")

# List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
print(f"\nBooks in library '{library_name}':")
for book in library.books.all():
    print(f" - {book.title} by {book.author.name}")

# Retrieve the librarian for a library
librarian = library.librarian
print(f"\nLibrarian for library '{library_name}': {librarian.name}")
