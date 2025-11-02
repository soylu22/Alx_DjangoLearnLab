```python
from bookshelf.models import Book

# Retrieve a book
book = Book.objects.get(title="1984")

# Delete the book
book.delete()

# Confirm deletion
Book.objects.all()
```

```
(1, {'bookshelf.Book': 1})
<QuerySet []>
```
