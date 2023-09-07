function removeProjectInvalid() {
    document.getElementById('project').setAttribute('class', 'form-control');
}

function removeAboutInvalid() {
    document.getElementById('about').setAttribute('class', 'form-control');
}

function createProject() {
    let name = document.getElementById('project').value;
    let about = document.getElementById('about').value;
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
        url: '/projects/?act=create',
        data: {
            'name': name,
            'about': about,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        async: false,
        success: function () {
            window.location.href = '/projects';
        }
    });
}