from django import forms
from .models import Book, Review


class BookForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Title",
            }
        )
    )
    author = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Author",
            }
        )
    )
    genre = forms.ChoiceField(
        choices=Book.Genre.choices,
        widget=forms.Select(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Genre",
            }
        ),
    )
    description = forms.CharField(
        required=False, 
        widget=forms.Textarea(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Description",
                "cols": 80,
            }
        )
    )

    class Meta:
        model = Book
        fields = ("title", "author", "genre", "description")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "review_text")
        widgets = {
            "review_text": forms.Textarea(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Write your review...",
                    "cols": 80,
                }
            )
        }
