"""Defines URL patterns for read_up"""

from django.urls import path
from . import views

app_name = "read_up"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    # Page that shows all topics
    path("books/", views.books, name="books"),
    # Detail page for a single topic.
    path("books/<int:book_id>/", views.book, name="book"),
    # Page for adding a new topic.
    path("new_book/", views.new_book, name="new_book"),
    # Page for deleting a book
    path("delete_book/<int:book_id>", views.delete_book, name="delete_book"),
    # Page for adding a review.
    path("add_review/<int:book_id>/", views.add_review, name="add_review"),
    # Page for editing a review.
    path("edit_review/<int:review_id>/", views.edit_review, name="edit_review"),
]
