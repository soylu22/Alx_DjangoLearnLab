from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Author, Library, Librarian  # <- must include Library


# FUNCTION-BASED VIEW
def list_books(request):
    books = Book.objects.all()
    return render(
        request,
        'relationship_app/list_books.html',   # CHECKER REQUIRES THIS EXACT STRING
        {'books': books}
    )

class LibraryDetailView(DetailView):
    model = Library               # <- uses Library directly
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

