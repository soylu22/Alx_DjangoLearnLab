#### **update.md**

````markdown
```python
book.title = "Nineteen Eighty-Four"
book.save()
book = Book.objects.get(id=book.id)
print(book.title)
# Output: Nineteen Eighty-Four
```
````
