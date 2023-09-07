from django.shortcuts import render, redirect
from Login.func import check_user, get_full_user_info, get_email, get_user_info


def profile(request):
    if not check_user(request):
        return redirect('/')
    return render(request, "user/profile.html", {'user': get_full_user_info(request.session['email'])})


def profile_by_id(request, user_id):
    if not check_user(request):
        return redirect('/')
    if not get_email("", user_id):
        return render(request, "user/profile_by_id.html", {'user': get_user_info(request.session['email']),
                                                           'not_found': 'True'})
    return render(request, "user/profile_by_id.html", {'user': get_user_info(request.session['email']),
                                                       'target': get_full_user_info(get_email("", user_id))})
