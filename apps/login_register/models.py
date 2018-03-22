# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.core.validators import RegexValidator
import bcrypt

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255, validators=[RegexValidator(
        regex=r'^[a-zA-Z]+$',
        message=("Name must contain letters only")
    )])
    last_name = models.CharField(max_length=255, validators=[RegexValidator(
        regex=r'^[a-zA-Z]+$',
        message=("Name must contain letters only")
    )])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def encrypt_password(self):
        self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
    def check_password(self, pw):
        return bcrypt.checkpw(pw.encode(), self.password.encode())

class UserRegForm(forms.ModelForm):
    first_name = forms.CharField(min_length=2)
    last_name = forms.CharField(min_length=2)
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