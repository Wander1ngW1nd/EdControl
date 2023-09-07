from django.http import HttpResponse
from django.shortcuts import render, redirect
from Login.func import check_user, get_user_info
from .models import Project
from Login.models import Users
from .func import get_project_info, get_projects


def projects(request):
    if not check_user(request):
        return redirect('/')
    if 'act' not in request.GET:
        projects_list = get_projects()
        return render(request, "projects/projects.html", {
            'user': get_user_info(request.session['email']),
            'projects': projects_list,
        })
    act = request.GET['act']
    if act == 'new_project':
        return render(request, "projects/new_project.html", {
            'user': get_user_info(request.session['email'])
        })
    if act == 'create':
        name = request.POST['name']
        about = request.POST['about']
        project = Project(name=name,
                          about=about,
                          owner=Users.objects.get(email=request.session['email']))
        project.save()
        return HttpResponse('ok')
    if act == 'view':
        project_id = request.GET['id']
        return render(request, "projects/project_by_id.html", {
            'user': get_user_info(request.session['email']),
            'project': get_project_info(project_id, Users.objects.get(email=request.session['email']).id),
        })
    if act == 'edit':
        project_id = request.GET['id']
        return render(request, "projects/edit_project.html", {
            'user': get_user_info(request.session['email']),
            'project': get_project_info(project_id, Users.objects.get(email=request.session['email']).id),
        })
    if act == 'edit_project':
        project_id = request.POST['id']
        name = request.POST['name']
        about = request.POST['about']
        project = Project.objects.get(id=project_id)
        if Users.objects.get(email=request.session['email']).id != project.owner.id:
            return HttpResponse('failed')
        project.name = name
        project.about = about
        project.save()
        return HttpResponse('ok')
    if act == 'delete_project':
        project_id = request.POST['id']
        project = Project.objects.get(id=project_id)
        if Users.objects.get(email=request.session['email']).id != project.owner.id:
            return HttpResponse('failed')
        project.delete()
        return HttpResponse('ok')
