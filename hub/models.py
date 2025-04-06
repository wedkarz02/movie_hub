from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def averate_rating(self):
        avg = self.rating_set.aggregate(models.Avg("score"))["score__avg"]
        return round(avg, 2) if avg else None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("hub-movie-details", kwargs={"pk": self.pk})


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    rated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} rated '{self.movie.title}' {self.score}/10"

    class Meta:
        unique_together = ("user", "movie")
