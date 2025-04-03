from django.shortcuts import render

counter = {
    "num": 0
}


def home(req):
    counter["num"] += 1
    context = {
        "counter": counter,
    }

    return render(req, "hub/home.html", context)


def about(req):
    return render(req, "hub/about.html", {"title": "About"})
