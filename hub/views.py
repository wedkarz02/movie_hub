from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Avg
from hub.models import Movie, Rating
from users.forms import RatingForm
from together import Together


class MovieListView(ListView):
    model = Movie
    template_name = "hub/movies.html"
    context_object_name = "movies"
    ordering = ["-updated_at"]

    def get_queryset(self):
        qs = super().get_queryset().annotate(
            avg_rating=Avg('rating__score')).order_by("-avg_rating")
        if self.request.user.is_authenticated:
            user_ratings = Rating.objects.filter(user=self.request.user)
            user_rating_dict = {r.movie_id: r.score for r in user_ratings}
            for movie in qs:
                movie.user_rating = user_rating_dict.get(movie.id)
        return qs


class MovieDetailView(DetailView):
    model = Movie
    template_name = "hub/movie_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.object

        avg = movie.rating_set.aggregate(Avg('score'))['score__avg']
        context['avg_rating'] = round(avg, 2) if avg else "No ratings yet"

        if self.request.user.is_authenticated:
            rating = Rating.objects.filter(
                user=self.request.user, movie=movie).first()
            context['rating_form'] = RatingForm(instance=rating)
            context['user_rating'] = rating.score if rating else None

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login')

        form = RatingForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                movie=self.object,
                defaults={'score': score}
            )
            return redirect(self.object.get_absolute_url())
        else:
            print("Rating form errors:", form.errors)
            context = self.get_context_data()
            context['rating_form'] = form
            return self.render_to_response(context)


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


@login_required
def delete_rating(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    rating = Rating.objects.filter(movie=movie, user=request.user).first()

    if rating:
        rating.delete()

    return redirect('hub-movie-details', pk=movie.id)


@login_required
def summarize_movie_description(req, pk):
    movie = get_object_or_404(Movie, id=pk)
    try:
        client = Together()
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {"role": "user", "content": f"Write a description of this movie: {movie}. Make it between at least 300 characters long. Make sure it's different every time I ask."}],
        )
        new_description = response.choices[0].message.content.strip()
        movie.description = new_description
        movie.save()

        if 'HX-Request' in req.headers:
            res = render(req, 'hub/partials/description_part.html',
                         {'movie': movie})
            res["HX-Trigger"] = "refreshPage"
            return res
        else:
            return redirect(req, "hub-movie-details", pk=pk)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def home(req):
    return render(req, "hub/home.html")


def about(req):
    return render(req, "hub/about.html", {"title": "About"})
