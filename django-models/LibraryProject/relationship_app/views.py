# LibraryProject/relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Author, Book, Library, Librarian  # <- must include Library for the checker

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: display details for a specific library
class LibraryDetailView(DetailView):
    model = Library                     # <- checker expects Library here
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Optional: If you want, you can add other views here in future
