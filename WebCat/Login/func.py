import datetime
import pytz
from django.utils import timezone
from .models import Users, UserInfo
import hashlib
import os
from base64 import b64encode

utc = pytz.UTC
timeout = datetime.timedelta(minutes=5)


def check_user(request):
    try:
        if not Users.objects.filter(email=request.session["email"], access_token=request.session["access_token"]):
            return False
        update_last_seen(request.session["email"])
        return True
    except KeyError:
        pass
    t = request.COOKIES
    try:
        if Users.objects.filter(email=t["login"], access_token=t["access_token"]):
            request.session["login"] = t["login"]
            request.session["access_token"] = t["access_token"]
            update_last_seen(request.session["email"])
            return True
    except KeyError:
        return False
    update_last_seen(request.session["email"])
    return True


def hash_pwd(email, password):
    salt = Users.objects.get(email=email)
    salt = salt.salt
    password += salt
    encrypt_password = hashlib.sha256()
    encrypt_password.update(password.encode("utf-8"))
    encrypt_password = encrypt_password.digest()
    return encrypt_password


def create_salt():
    salt = os.urandom(256)
    salt = b64encode(salt).decode("utf-8")
    return salt


def create_user(email, login, password, name, surname, organization, about):
    if Users.objects.filter(email=email):
        return "False email"
    if Users.objects.filter(login=login):
        return "False login"
    salt = create_salt()
    user = Users(
        email=email,
        login=login,
        salt=salt,
        join_date=datetime.datetime.now(),
        last_seen=datetime.datetime.now(),
        user_status="user",
        access_level=0,
    )
    user.save()
    password = hash_pwd(email, password)
    user.password = password
    user.save()
    user_info = UserInfo(name=name, surname=surname, organization=organization, about=about, user=user)
    user_info.save()
    return True


def check_authorize(email, password, access_token=None):
    if access_token:
        if not Users.objects.filter(email=email, access_token=access_token):
            return False
        return True
    if "@" not in email:
        email = Users.objects.get(login=email).email
    if not Users.objects.filter(email=email):
        return False
    encrypt_password = hash_pwd(email, password)
    if not Users.objects.filter(email=email, password=encrypt_password):
        return False
    access_token = os.urandom(512)
    access_token = b64encode(access_token).decode("utf-8")
    set_access_token(email, access_token)
    return access_token


def set_access_token(email, access_token):
    user = Users.objects.get(email=email)
    user.access_token = access_token
    user.save()


def get_email(login, user_id=None):
    if user_id:
        if not Users.objects.filter(id=user_id):
            return False
        return Users.objects.get(id=user_id).email
    return Users.objects.get(login=login).email


def get_user_info(email):
    model_user_info = UserInfo.objects.get(user=Users.objects.get(email=email).id)
    user = {
        "name": model_user_info.name,
    }
    return user


def get_full_user_info(email):
    model_user_info = UserInfo.objects.get(user=Users.objects.get(email=email).id)
    model_user = Users.objects.get(email=email)
    user = {
        "name": model_user_info.name,
        "surname": model_user_info.surname,
        "id": model_user.id,
        "email": email,
        "about": model_user_info.about,
        "join_date": model_user.join_date.strftime("%b %d, %Y"),
        "last_seen": is_online(model_user.last_seen),
        "user_status": model_user.user_status,
    }
    return user


def update_last_seen(email):
    time = datetime.datetime.now()
    user = Users.objects.get(email=email)
    user.last_seen = time
    user.save()


def is_online(time):
    print(time)
    if time + timeout < timezone.now():
        time = timezone.now() - time
        if time < datetime.timedelta(minutes=1):
            time = str(time.seconds)
            if time == "1":
                time += " second"
            else:
                time += " seconds"
        elif time < datetime.timedelta(hours=1):
            time = str((time.seconds // 60) % 60)
            if time == "1":
                time += " minute"
            else:
                time += " minutes"
        elif time < datetime.timedelta(days=1):
            time = str(time.seconds // 3600)
            if time == "1":
                time += " hour"
            else:
                time += " hours"
        else:
            time = str(time.days)
            if time == "1":
                time += " day"
            else:
                time += " day"
        return time
    return "Online"
