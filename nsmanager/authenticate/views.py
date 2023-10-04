# authenticate/views.py

from django.contrib.auth import views as auth_views
from .forms import RegistrationForm 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class LoginView(auth_views.LoginView):
    template_name = 'login.html'

class LogoutView(auth_views.LogoutView):
    next_page = 'authenticate:login'  # Przekierowanie po wylogowaniu
    template_name = 'logout.html'

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('authenticate:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Rejestracja przebiegła pomyślnie!')
        return response

