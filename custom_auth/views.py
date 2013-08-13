from django.contrib.auth import logout as logout_user

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .forms import RegistrationForm, LoginForm
from .models import User


def register(request, template_name='auser/register.html'):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #process the form
            email = request.POST.get('email', None)
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            password = request.POST.get('password', None)
            user = User.objects.create_user(email, first_name, last_name, password)
            return redirect('registration_successful')
    else:
        form = RegistrationForm()
    return render_to_response(template_name, {'form': form,}, RequestContext(request))


def registration_successful(request, template_name='auser/registration_successful.html'):
    return render_to_response(template_name, RequestContext(request))


def activate(request, template_name='auser/activate.html'):
    form = RegistrationForm()
    return render_to_response(template_name, {'form': form,}, RequestContext(request))


def login(request, template_name='auser/login.html'):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.login(request):
            return redirect('manage_home')
    else:
        form = LoginForm()
    return render_to_response(template_name, {'form': form,}, RequestContext(request))


def logout(request):
    logout_user(request)
    return redirect('auth_login')