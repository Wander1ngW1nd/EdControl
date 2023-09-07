from django.shortcuts import render
from Login.func import check_user, get_user_info


def main(request):
    if not check_user(request):
        user = {
            'not_auth': 'True'
        }
        return render(request, 'main/index.html', {'user': user})
    return render(request, 'main/index.html', {'user': get_user_info(request.session['email'])})
