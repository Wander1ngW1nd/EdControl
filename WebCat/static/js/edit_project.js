function saveProject() {
    let name = document.getElementById('project').value;
    let about = document.getElementById('about').value;
    let project_id = document.getElementById('id').value;
    if (name === '' || about === '') {
        if (name === '') {
            document.getElementById('project').setAttribute('class', 'form-control is-invalid');
        }
        if (about === '') {
            document.getElementById('about').setAttribute('class', 'form-control is-invalid');
        }
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/projects/?act=edit_project',
        data: {
            'name': name,
            'about': about,
            'id': project_id,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        async: false,
        success: function () {
            window.location.href = '/projects';
        }
    });
}

function deleteProject() {
    let project_id = document.getElementById('id').value;
    $.ajax({
        type: 'POST',
        url: '/projects/?act=delete_project',
        data: {
            'id': project_id,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        async: false,
        success: function () {
            window.location.href = '/projects';
        }
    });
}