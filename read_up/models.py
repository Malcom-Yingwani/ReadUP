from django.contrib.auth.models import User
from django.db import models


from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    """A book the user is reading."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="books",  # lets us do user..all()
    )
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    # Creates a drop down field of choices
    class Genre(models.TextChoices):
        THEOLOGY = "TH", _("Theology")
        CHRISTIAN_LITERATURE = "CL", _("Christian Literature")
        FANTASY = "FS", _("Fantasy")
        SCI_FI = "Sci_Fi", _("Science Fiction")
        MYSTERY = "MY", _("Mystery")
        THRILLER = "THR", _("Thriller")
        HORROR = "HR", _("Horror")
        ROMANCE = "RM", _("Romance")
        HISTORICAL_FICTION = "HF", _("Historical Fiction")
        LITERARY_FICTION = "LF", _("Literary Fiction")
        ADVENTURE = "ADV", _("Adventure")
        CONTEMPORARY = "CT", _("Contemporary Fiction")
        MAGICAL_REALISM = "MR", _("Magical Realism")
        CRIME = "CR", _("Crime / Detective")
        YOUNG_ADULT = "YA", _("Young Adult")
        NEW_ADULT = "NA", _("New Adult")
        BIOGRAPHY = "BIO", _("Biography")
        MEMOIR = "MEM", _("Memoir")
        SELF_HELP = "SH", _("Self-Help")
        HISTORY = "HIS", _("History")
        PHILOSOPHY = "PHI", _("Philosophy")
        TRUE_CRIME = "TC", _("True Crime")
        RELIGION_SPIRITUALITY = "RS", _("Religion & Spirituality")
        BUSINESS = "BUS", _("Business & Economics")
        PSYCHOLOGY = "PSY", _("Psychology")
        SCIENCE = "SCI", _("Science & Technology")
        OTHER = "OTH", _("Other")

    genre = models.CharField(
        choices=Genre.choices,
        default=Genre.THEOLOGY,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "title", "author")

    def __str__(self):
        """Return a simple string representing the book."""
        return f"{self.title} <{self.author}>"


class Review(models.Model):
    """A user written review"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Stars(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"

    rating = models.PositiveSmallIntegerField(choices=Stars.choices)
    review_text = models.TextField(blank=True)
    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        """Return a simple string representing the review"""
        if len(self.review_text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.review_text}"
