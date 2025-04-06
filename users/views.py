from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hub.models import Rating
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(req):
    if req.method == "POST":
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                req, f"Account has been created for {username}! Please log in.")
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(req, "users/register.html", {"form": form, "title": "Register"})


@login_required
def profile(req):
    if req.method == "POST":
        u_form = UserUpdateForm(req.POST, instance=req.user)
        p_form = ProfileUpdateForm(
            req.POST, req.FILES, instance=req.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                req, f"Profile info has been updated.")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=req.user)
        p_form = ProfileUpdateForm(instance=req.user.profile)

    rated = req.user.profile.rated_movies().annotate(
        user_score=Subquery(
            Rating.objects.filter(user=req.user, movie=OuterRef('pk'))
            .values('score')[:1]
        ),
        avg_rating=Avg('rating__score')
    )

    context = {
        "u_form": u_form,
        "p_form": p_form,
        "rated_movies": rated,
        "title": req.user.profile
    }

    return render(req, "users/profile.html", context)
