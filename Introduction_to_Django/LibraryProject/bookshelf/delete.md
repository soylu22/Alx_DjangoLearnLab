```python
from bookshelf.models import Book
books = Book.objects.all()
books
books.delete()
Book.objects.all()
```

```
<QuerySet [<Book: 1984 by George Orwell (1949)>]>
(1, {'bookshelf.Book': 1})
<QuerySet []>
```
