from .models import Project


def get_project_info(project_id, user_id):
    project = Project.objects.get(id=project_id)
    return {
        'name': project.name,
        'owner': project.owner.login,
        'about': project.about,
        'is_owner': user_id == project.owner.id,
        'id': project.id,
    }


def get_projects():
    res_projects = []
    projects = Project.objects.all()
    i = 1
    for project in projects:
        res_projects.append({
            'name': project.name,
            'about': project.about,
            'owner': project.owner.login,
            'id': project.id,
            'number': i,
        })
        i += 1
    return res_projects
