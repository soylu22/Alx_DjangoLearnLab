from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book, Library


# Book Views with Permission Checks
@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """
    View all books - requires can_view_book permission
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """
    Create a new book - requires can_create_book permission
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')

        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            created_by=request.user
        )
        messages.success(request, f'Book "{book.title}" created successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/book_form.html')


@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, book_id):
    """
    Edit a book - requires can_edit_book permission
    """
    book = get_object_or_404(Book, id=book_id)

    # Additional check: users can only edit their own books unless they're superusers
    if book.created_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only edit books you created.")

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.save()
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/book_form.html', {'book': book})


@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, book_id):
    """
    Delete a book - requires can_delete_book permission
    """
    book = get_object_or_404(Book, id=book_id)

    # Additional check: users can only delete their own books unless they're superusers
    if book.created_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete books you created.")

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# Library Views
@login_required
@permission_required('bookshelf.can_view_library', raise_exception=True)
def library_list(request):
    """
    View all libraries - requires can_view_library permission
    """
    libraries = Library.objects.all()
    return render(request, 'bookshelf/library_list.html', {'libraries': libraries})


def user_dashboard(request):
    """
    User dashboard showing their permissions and books
    """
    user_books = Book.objects.filter(created_by=request.user)
    user_permissions = request.user.get_all_permissions()

    return render(request, 'bookshelf/dashboard.html', {
        'user_books': user_books,
        'user_permissions': user_permissions
    })