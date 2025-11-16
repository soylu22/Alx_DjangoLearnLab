from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q
from .models import Book, Library


# Secure book list view with proper query parameterization
@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """
    View all books with secure search functionality.
    Uses Django ORM to prevent SQL injection attacks.
    """
    # Secure search implementation using Django ORM
    # This prevents SQL injection by using parameterized queries
    search_query = request.GET.get('search', '').strip()

    if search_query:
        # Safe query using Django ORM - no string formatting in queries
        books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    else:
        books = Book.objects.all()

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })


@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """
    Create a new book with input validation.
    Uses CSRF protection via template token.
    """
    if request.method == 'POST':
        # Input validation and sanitization
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        description = request.POST.get('description', '').strip()

        # Validate required fields
        if not title or not author:
            messages.error(request, 'Title and author are required fields.')
            return render(request, 'bookshelf/form_example.html')

        # Input length validation to prevent buffer overflow attacks
        if len(title) > 200:
            messages.error(request, 'Title is too long (maximum 200 characters).')
            return render(request, 'bookshelf/form_example.html')

        if len(author) > 100:
            messages.error(request, 'Author name is too long (maximum 100 characters).')
            return render(request, 'bookshelf/form_example.html')

        # Create book using Django ORM (safe from SQL injection)
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            created_by=request.user
        )
        messages.success(request, f'Book "{book.title}" created successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/form_example.html')


@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, book_id):
    """
    Edit a book with proper authorization checks.
    Uses get_object_or_404 for safe object retrieval.
    """
    # Safe object retrieval - prevents exposure of non-existent objects
    book = get_object_or_404(Book, id=book_id)

    # Authorization check - users can only edit their own books
    if book.created_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only edit books you created.")

    if request.method == 'POST':
        # Input validation and sanitization
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        description = request.POST.get('description', '').strip()

        # Validate required fields
        if not title or not author:
            messages.error(request, 'Title and author are required fields.')
            return render(request, 'bookshelf/form_example.html', {'book': book})

        # Input length validation
        if len(title) > 200:
            messages.error(request, 'Title is too long (maximum 200 characters).')
            return render(request, 'bookshelf/form_example.html', {'book': book})

        if len(author) > 100:
            messages.error(request, 'Author name is too long (maximum 100 characters).')
            return render(request, 'bookshelf/form_example.html', {'book': book})

        # Safe update using Django ORM
        book.title = title
        book.author = author
        book.description = description
        book.save()

        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/form_example.html', {'book': book})


@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, book_id):
    """
    Delete a book with proper authorization.
    Uses POST method for destructive operations.
    """
    # Safe object retrieval
    book = get_object_or_404(Book, id=book_id)

    # Authorization check
    if book.created_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete books you created.")

    if request.method == 'POST':
        # Safe deletion using Django ORM
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# Secure library view with proper query handling
@login_required
@permission_required('bookshelf.can_view_library', raise_exception=True)
def library_list(request):
    """
    View all libraries with secure data access.
    """
    # Safe query using Django ORM
    libraries = Library.objects.all()
    return render(request, 'bookshelf/library_list.html', {'libraries': libraries})


def user_dashboard(request):
    """
    User dashboard with secure data access.
    """
    # Safe queries using Django ORM
    user_books = Book.objects.filter(created_by=request.user)
    user_permissions = request.user.get_all_permissions()

    return render(request, 'bookshelf/dashboard.html', {
        'user_books': user_books,
        'user_permissions': user_permissions
    })


# SECURITY TESTING CHECKLIST:
# 1. Test forms without CSRF token - should be rejected
# 2. Test SQL injection attempts in search fields - should be safely handled
# 3. Test XSS attempts in input fields - should be properly escaped
# 4. Verify HTTPS-only cookies in production
# 5. Test authorization boundaries - users should only access their own data
# 6. Test permission-based access control
# 7. Verify input validation and sanitization