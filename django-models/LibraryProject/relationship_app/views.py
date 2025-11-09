from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

# Add book (requires can_add_book permission)
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            from .models import Author
            author = Author.objects.get(id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')
    from .models import Author
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

# Edit book (requires can_change_book permission)
@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        author_id = request.POST.get('author')
        if author_id:
            from .models import Author
            book.author = Author.objects.get(id=author_id)
        book.save()
        return redirect('list_books')
    from .models import Author
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})

# Delete book (requires can_delete_book permission)
@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
