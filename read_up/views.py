from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods


from .forms import BookForm, ReviewForm
from .models import Book, Review


# Create your views here.
def index(request):
    """The home page for Read UP."""
    return render(request, "index.html")


# Book logic


@login_required
def books(request):
    """Show all topics"""
    books = Book.objects.filter(user=request.user).order_by("title")
    form = BookForm()
    context = {"books": books, "form": form}
    return render(request, "books.html", context)


@login_required
def book(request, book_id):
    """Show a single book and it's details & review"""
    book = Book.objects.get(id=book_id)
    # Make sure the book belongs to the user.
    if book.user != request.user:
        raise Http404("You do not have permission to view this book.")
    else:
        # Get the user's review for this book, if it exists
        try:
            review = Review.objects.get(book=book, user=request.user)
        except Review.DoesNotExist:
            review = None

    context = {
        "book": book,
        "review": review,
    }
    return render(request, "book_detail.html", context)


@login_required
@require_http_methods(["POST"])
def new_book(request):
    """Add a new book"""
    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.user = request.user
        book.save()
        # Return partial containing a new row for our user
        # that wecan add to the table
        context = {"book": book}
        response = render(request, "partials/book_row.html", context)
        response["HX-Trigger"] = "success"
        return response
    else:
        context = {"form": form}
        response = render(request, "partials/add_book_modal.html", {"form": form})
        response["HX-Retarget"] = "#book-modal"
        response["HX-Reswap"] = "outerHTML"
        response["HX-Trigger-After-Settle"] = "fail"
        return response


@login_required
@require_http_methods(["DELETE"])
def delete_book(request, book_id):
    """Delete existing book."""
    book = get_object_or_404(Book, id=book_id, user=request.user)
    book.delete()
    if request.method == "DELETE":
        response = redirect("read_up:books")
        response["HX-Trigger"] = "book-deleted"
        return response

    return render(request, "delete_book.html", {"book": book})


#  Review Logic


@login_required
def add_review(request, book_id):
    """Add a review for a particular book."""
    book = Book.objects.get(id=book_id)

    if request.method != "POST":
        # No data submitted; process data.
        form = ReviewForm()
    else:
        # Post data submitted; process data.
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()
            return redirect("read_up:book", book_id=book_id)

    # Display a blank or invalid form.
    context = {"book": book, "form": form}
    return render(request, "add_review.html", context)


@login_required
def edit_review(request, review_id):
    """Edit an existing review."""
    review = Review.objects.get(id=review_id)
    book = review.book
    if book.user != request.user:
        raise Http404

    if request.method != "POST":
        # Initial request; pre-fill form with the currently entry.
        form = ReviewForm(instance=review)
    else:
        # POST data submitted; process data.
        form = ReviewForm(instance=review, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("read_up:book", book_id=book.id)

    context = {"review": review, "book": book, "form": form}
    return render(request, "edit_review.html", context)
