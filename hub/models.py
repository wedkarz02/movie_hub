from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
