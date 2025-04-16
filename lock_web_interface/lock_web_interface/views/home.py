from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login as lg, logout as lo
import logging

from django.urls import reverse

from lock_web_interface.forms.user_form import AdminForm

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "lock_web_interface/home.html")


def login(request):
    if request.method == "GET":
        return render(request, 'lock_web_interface/login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.user_type == "ADMIN":
            lg(request, user)
            return HttpResponseRedirect(reverse('management'))
        else:
            logger.info('Login failed')
            context = {
                "error": "Email et/ou Mot de passe incorrect"
            }
            return render(request, 'lock_web_interface/login.html', context)
    else:
        logger.info("method not allowed")
        return HttpResponse(405)


def logout(request):
    """
    This function deletes the current user session and log him out
    :param request:
    :return: return an HttpResponse
    """
    lo(request)
    return HttpResponseRedirect(reverse('login'))


def signup(request):
    """
    This function process GET and POST request for signup view
    :param request:
    :return: return an HttpResponse
    """
    if request.method == "GET":
        form = AdminForm()
        return render(request, 'lock_web_interface/signup.html', context={'form': form})
    elif request.method == "POST":
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('management_users'))
        else:
            logger.error(form.errors)
            return render(request, 'lock_web_interface/signup.html', context={'form': form})
    else:
        logger.info("method not allowed")
        return HttpResponse(405)


def reset_password(request):
    pass
