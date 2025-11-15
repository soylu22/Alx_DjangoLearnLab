from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# FUNCTION-BASED VIEW
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# CLASS-BASED VIEW
class LibraryDetailView(DetailView):
    model = Library                           # Show a single Library
    template_name = 'library_detail.html'     # Template to use
    context_object_name = 'library'           # Name used in the template
