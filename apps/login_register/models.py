# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
import bcrypt

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def validate_letters(value):
    if not value.isalpha():
        raise forms.ValidationError("Letters only")

class UserRegForm(forms.ModelForm):
    first_name = forms.CharField(min_length=2, validators=[validate_letters])
    last_name = forms.CharField(min_length=2, validators=[validate_letters])
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password"
        ]
    def clean(self):
        cleaned_data = super(UserRegForm, self).clean()
        pw = cleaned_data.get("password")
        pc = cleaned_data.get("confirm_password")
        if pw != pc:
            raise forms.ValidationError("Password does not match")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)