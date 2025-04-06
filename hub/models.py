from django.db import models
from django.utils import timezone
from django.urls import reverse


class Movie(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    # ratings_sum = models.IntegerField()
    # ratings_ctr = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    # def rating(self):
    #     return round(self.ratings_sum / self.ratings_ctr, 2)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("hub-movie-details", kwargs={"pk": self.pk})
