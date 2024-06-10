from django import forms
from django.contrib.auth.models import User
from werkzeug.security import generate_password_hash
from django.contrib.auth.hashers import make_password


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        hashed_password = make_password(self.cleaned_data['password'])  # Parolni hash qilish
        user.password = hashed_password
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password']

