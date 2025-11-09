import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def ensure_sample_data():
    if Author.objects.exists():
        return
    a1 = Author.objects.create(name='Chinua Achebe')
    a2 = Author.objects.create(name='Toni Morrison')

    b1 = Book.objects.create(title='Things Fall Apart', author=a1)
    b2 = Book.objects.create(title='No Longer at Ease', author=a1)
    b3 = Book.objects.create(title='Beloved', author=a2)

    lib1 = Library.objects.create(name='Central Library')
    lib2 = Library.objects.create(name='Community Library')

    lib1.books.add(b1, b3)
    lib2.books.add(b2)

    Librarian.objects.create(name='Alice Johnson', library=lib1)
    Librarian.objects.create(name='Samuel K.', library=lib2)

def books_by_author(author_name):
    print(f"Books by {author_name}:")
    for b in Book.objects.filter(author__name=author_name):
        print(f" - {b.title}")

def books_in_library(library_name):
    lib = Library.objects.get(name=library_name)
    print(f"Books in library '{library_name}':")
    for b in lib.books.all():
        print(f" - {b.title} by {b.author.name}")

def librarian_for_library(library_name):
    lib = Library.objects.get(name=library_name)
    print(f"Librarian for library '{library_name}': {lib.librarian.name}")

if __name__ == '__main__':
    ensure_sample_data()
    books_by_author('Chinua Achebe')
    print()
    books_in_library('Central Library')
    print()
    librarian_for_library('Central Library')
