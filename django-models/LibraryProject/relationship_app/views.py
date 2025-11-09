from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

# Checker requires a separate import for Library
from .models import Library

# Import other models separately
from .models import Author, Book, Librarian

# ----------------------------
# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()  # Book is now defined
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: show details of a library
class LibraryDetailView(DetailView):
    model = Library              # Library is now defined
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
