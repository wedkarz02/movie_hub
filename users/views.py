from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(req):
    if req.method == "POST":
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(req, f"Account created for {username}")
            return redirect("hub-home")
    else:
        form = UserRegisterForm()

    return render(req, "users/register.html", {"form": form, "title": "Register"})
