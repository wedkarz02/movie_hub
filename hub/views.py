from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from hub.models import Movie


class MovieListView(ListView):
    model = Movie
    template_name = "hub/movies.html"
    context_object_name = "movies"
    ordering = ["-updated_at"]


class MovieDetailView(DetailView):
    model = Movie
    template_name = "hub/movie_details.html"


class MovieCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Movie
    template_name = "hub/movie_form.html"
    fields = ["title", "year"]

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.warning(
            self.request, "You are not authorized to view this page.")
        return redirect("hub-home")


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    template_name = "hub/movie_form.html"
    fields = ["title", "year"]

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.warning(
            self.request, "You are not authorized to view this page.")
        return redirect("hub-home")


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    success_url = "/movies"
    template_name = "hub/movie_delete.html"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.warning(
            self.request, "You are not authorized to view this page.")
        return redirect("hub-home")


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
