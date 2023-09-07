function authorize()  {
    let email = document.getElementById("authEmail").value;
    let password = document.getElementById("authPassword").value;
    let token;
    $.ajax({
        type: 'POST',
        url: '/check_authorize/',
        data: {
            'email': email,
            'password': password,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        async: false,
        success: function (data) {
            if (data === "False") {
                document.getElementById("authError").removeAttribute("hidden");
            } else {
                token = data;
            }
        }
    });
    $.ajax({
        type: 'POST',
        url: '/set_session_variable/',
        data: {
            'type': 'auth',
            'email': email,
            'access_token': token,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        async: false,
        success: function (data) {
            if (data === 'ok') {
                window.location.href = '/';
            } else {
                document.getElementById("authError").removeAttribute("hidden");
            }
        }
    })
}

function logOut() {
    $.ajax({
        type: 'POST',
        url: '/log_out/',
        data: {'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
        async: false,
        success: function () {
            window.location.href = '/';
        }
    })
}