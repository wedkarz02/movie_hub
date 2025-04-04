from django.shortcuts import render

from hub.models import Movie

counter = {
    "num": 0
}


def home(req):
    counter["num"] += 1
    context = {
        "counter": counter,
    }

    return render(req, "hub/home.html", context)


def movies(req):
    context = {
        "movies": Movie.objects.all(),
        "title": "Movies",
    }
    return render(req, "hub/movies.html", context)


def about(req):
    return render(req, "hub/about.html", {"title": "About"})
