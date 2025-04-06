from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from hub.models import Rating
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["score"]
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'step': 1,
                'placeholder': 'Rate from 1 to 10',
                'style': 'width: 200px; height: 40px;'
            })
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if not score:
            raise forms.ValidationError("Please enter a rating.")
        if score < 1 or score > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return score
