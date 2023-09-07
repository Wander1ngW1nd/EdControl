from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .func import create_user, check_authorize, get_email, check_user


def sign_up(request):
    if check_user(request):
        return redirect("/profile")
    return render(request, "login/sign.html")


def check_email(request):
    email = request.POST["email"]
    token = get_random_string(length=16)
    send_mail(
        "Registration code",
        "Your code: " + token,
        "webcatbot@yandex.ru",
        [email],
    )
    return render(request, "login/token.html", {"token": token})


def register(request):
    email = request.POST["email"]
    login = request.POST["login"]
    password = request.POST["password"]
    name = request.POST["name"]
    surname = request.POST["surname"]
    organization = request.POST["organization"]
    about = request.POST["about"]
    reply = create_user(email, login, password, name, surname, organization, about)
    if reply != "False email" or reply != "False login":
        return render(request, "login/register.html", {"status": "ok"})
    return render(request, "login/register.html", {"status": reply})


def authorize(request):
    email = request.POST["email"]
    password = request.POST["password"]
    access_token = check_authorize(email, password)
    if not access_token:
        return render(request, "login/token.html", {"token": "False"})
    return render(request, "login/token.html", {"token": access_token})


def test(request):
    temp = request.session["test"]
    return render(request, "login/test.html", {"test": temp})


def set_session_variable(request):
    req_type = request.POST["type"]
    if req_type == "auth":
        email = request.POST["email"]
        access_token = request.POST["access_token"]
        if "@" not in email:
            email = get_email(email)
        request.session["email"] = email
        request.session["access_token"] = access_token
        return HttpResponse("ok")
    return HttpResponse("failed")


def log_out(request):
    del request.session["email"]
    del request.session["access_token"]
    return HttpResponse("ok")
