from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Book, Library
from django.views.generic.detail import DetailView

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'