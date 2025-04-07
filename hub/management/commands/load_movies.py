import json
from django.core.management.base import BaseCommand
from hub.models import Movie


class Command(BaseCommand):
    help = "Load movie data from JSON file"

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str,
                            help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                title = item.get('title')
                year = item.get('year')
                if title and year:
                    movie, created = Movie.objects.get_or_create(
                        title=title, year=year)
                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f"Added movie: {title} ({year})"))
                    else:
                        self.stdout.write(
                            f"Movie already exists: {title} ({year})")
