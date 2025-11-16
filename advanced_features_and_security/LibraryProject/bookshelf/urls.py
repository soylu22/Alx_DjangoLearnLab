from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('libraries/', views.library_list, name='library_list'),
]