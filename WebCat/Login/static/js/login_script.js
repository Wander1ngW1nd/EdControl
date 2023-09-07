let emailOk = false;
let yearOk  = false;
let token = null;
let customLogin = false;
let rejectTime;

function checkEmail() {
    let email = document.getElementById("email").value;
    let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (email === "") {
        emailOk = false;
        document.getElementById("email").setAttribute("class", "form-control");
    } else if (re.test(String(email).toLowerCase())) {
        emailOk = true;
        document.getElementById("email").setAttribute("class", "form-control is-valid");
    } else {
        emailOk = false;
        document.getElementById("email").setAttribute("class", "form-control is-invalid");
    }
    if (!customLogin) {
        fillLogin();
    }
}

function removeYearInvalid() {
    document.getElementById("year").setAttribute("class", "form-check-input");
    yearOk = !yearOk;
}

function removePasswordInvalid() {
    document.getElementById("passwordFirst").setAttribute("class", "form-control");
}

function removePasswordConfirmInvalid() {
    if (!validatePassConfirm() && document.getElementById("passwordConfirm").value !== "") {
        return;
    }
    document.getElementById("passwordConfirm").setAttribute("class", "form-control");
}

function removeNameInvalid() {
    document.getElementById("name").setAttribute("class", "form-control");
}

function removeSurNameInvalid() {
    document.getElementById("surname").setAttribute("class", "form-control");
}

function removeOrganizationInvalid() {
    document.getElementById("organization").setAttribute("class", "form-control");
}

function removeAboutInvalid() {
    document.getElementById("about").setAttribute("class", "form-control");
}

function validatePassConfirm() {
    let password = document.getElementById("passwordFirst").value;
    let passwordConfirm = document.getElementById("passwordConfirm").value;
    if (passwordConfirm === "") {
        document.getElementById("passwordConfEmpty").removeAttribute("hidden");
        if (password === "") {
            document.getElementById("notSamePasswords").setAttribute("hidden", "true");
        } else {
            document.getElementById("notSamePasswords").removeAttribute("hidden");
            document.getElementById("passwordConfirm").setAttribute("class", "form-control is-invalid");s
        }
        return false;
    } else {
        document.getElementById("passwordConfEmpty").setAttribute("hidden", "true");
    }
    if (password !== passwordConfirm) {
        document.getElementById("passwordConfirm").setAttribute("class", "form-control is-invalid");
        document.getElementById("notSamePasswords").removeAttribute("hidden");
        return false;
    } else {
        document.getElementById("passwordConfirm").setAttribute("class", "form-control");
        document.getElementById("notSamePasswords").setAttribute("hidden", "true");
        return true;
    }
}

function removeEmailInvalid() {
    if (document.getElementById("email").value === "") {
        document.getElementById("email").setAttribute("class", "form-control");
    }
    document.getElementById("existsEmail").setAttribute("hidden", "true");
    document.getElementById("emailTypeError").removeAttribute("hidden");
}

function removeLoginInvalid() {
    document.getElementById("existsLogin").setAttribute("hidden", "true");
    if (!customLogin) {
        return;
    }
    document.getElementById("login").setAttribute("class", "form-control");
    document.getElementById("existsLogin").setAttribute("hidden", "true");
    document.getElementById("emptyLogin").removeAttribute("hidden");
}

function removeTokenInvalid() {
    document.getElementById("emailToken").setAttribute("class", "form-control");
}

function continueReg() {
    if (document.getElementById("nameDiv").hasAttribute("hidden")) {
        if (!validatePassConfirm() || !emailOk || !yearOk || document.getElementById("passwordFirst").value === "" || document.getElementById("passwordConfirm").value === "" || document.getElementById("login").value === "") {
            if (!yearOk) {
                document.getElementById("year").setAttribute("class", "form-check-input is-invalid");
            }
            if (!emailOk) {
                document.getElementById("email").setAttribute("class", "form-control is-invalid");
            }
            if (document.getElementById("passwordFirst").value === "") {
                document.getElementById("passwordFirst").setAttribute("class", "form-control is-invalid");
            }
            if (document.getElementById("passwordConfirm").value === "") {
                document.getElementById("passwordConfirm").setAttribute("class", "form-control is-invalid");
            }
            if (document.getElementById("login").value === "") {
                document.getElementById("login").setAttribute("class", "form-control is-invalid");
            }
            return;
        }
        document.getElementById("emailDiv").setAttribute("hidden", "true");
        document.getElementById("passwordDiv").setAttribute("hidden", "true");
        document.getElementById("passwordConfirmDiv").setAttribute("hidden", "true");
        document.getElementById("hrDiv").setAttribute("hidden", "true");
        document.getElementById("yearDiv").setAttribute("hidden", "true");
        document.getElementById("specDiv").setAttribute("hidden", "true");
        document.getElementById("loginDiv").setAttribute("hidden", "true");
        document.getElementById("nameDiv").removeAttribute("hidden");
        document.getElementById("surNameDiv").removeAttribute("hidden");
        document.getElementById("organizationDiv").removeAttribute("hidden");
        document.getElementById("aboutDiv").removeAttribute("hidden");
        document.getElementById("back").removeAttribute("hidden");
        document.getElementById("hint").innerHTML = "Step 2 - Personal information";
    } else {
        if (document.getElementById("name").value === "" || document.getElementById("surname").value === "" || document.getElementById("organization").value === "" || document.getElementById("about").value === "") {
            if (document.getElementById("name").value === "") {
                document.getElementById("name").setAttribute("class", "form-control is-invalid");
            }
            if (document.getElementById("surname").value === "") {
                document.getElementById("surname").setAttribute("class", "form-control is-invalid");
            }
            if (document.getElementById("organization").value === "") {
                document.getElementById("organization").setAttribute("class", "form-control is-invalid");
            }
            if (document.getElementById("about").value === "") {
                document.getElementById("about").setAttribute("class", "form-control is-invalid");
            }
            return;
        }
        document.getElementById("nameDiv").setAttribute("hidden", "true");
        document.getElementById("surNameDiv").setAttribute("hidden", "true");
        document.getElementById("organizationDiv").setAttribute("hidden", "true");
        document.getElementById("aboutDiv").setAttribute("hidden", "true");
        document.getElementById("continue").setAttribute("hidden", "true");
        document.getElementById("back").setAttribute("hidden", "true");
        document.getElementById("emailTokenDiv").removeAttribute("hidden");
        document.getElementById("finish").removeAttribute("hidden");
        document.getElementById("hint").innerHTML = "Step 3 - Email conformation";
        $.ajax({
            type: 'POST',
            url: '/check_email/',
            data: {
                "email": document.getElementById("email").value,
                "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
            },
            async: true,
            success: function (data) {
                token = data;
            }
        });
    }
}

function backReg() {
    if (document.getElementById("nameDiv").hasAttribute("hidden")) {
        document.getElementById("nameDiv").removeAttribute("hidden");
        document.getElementById("surNameDiv").removeAttribute("hidden");
        document.getElementById("organizationDiv").removeAttribute("hidden");
        document.getElementById("aboutDiv").removeAttribute("hidden");
        document.getElementById("continue").removeAttribute("hidden");
        document.getElementById("finish").setAttribute("hidden", "true");
        document.getElementById("emailTokenDiv").setAttribute("hidden", "true");
        document.getElementById("hint").innerHTML = "Step 2 - Personal information";
    } else {
        document.getElementById("emailDiv").removeAttribute("hidden");
        document.getElementById("passwordDiv").removeAttribute("hidden");
        document.getElementById("passwordConfirmDiv").removeAttribute("hidden");
        document.getElementById("hrDiv").removeAttribute("hidden");
        document.getElementById("yearDiv").removeAttribute("hidden");
        document.getElementById("specDiv").removeAttribute("hidden");
        document.getElementById("loginDiv").removeAttribute("hidden");
        document.getElementById("nameDiv").setAttribute("hidden", "true");
        document.getElementById("surNameDiv").setAttribute("hidden", "true");
        document.getElementById("organizationDiv").setAttribute("hidden", "true");
        document.getElementById("aboutDiv").setAttribute("hidden", "true");
        document.getElementById("back").setAttribute("hidden", "true");
        document.getElementById("hint").innerHTML = "Step 1 - Account information";
    }
}

function isOk() {
    return false;
}

function setOk() {
    let userToken = document.getElementById("emailToken").value;
    if (userToken !== token) {
        document.getElementById("emailToken").setAttribute("class", "form-control is-invalid");
    } else {
        document.getElementById("emailToken").setAttribute("class", "form-control");
        let answer = "!ok";
        $.ajax({
            type: 'POST',
            url: '/register/',
            data: {
                "email": document.getElementById("email").value,
                "login": document.getElementById("login").value,
                "password": document.getElementById("passwordFirst").value,
                "name": document.getElementById("name").value,
                "surname": document.getElementById("surname").value,
                "organization": document.getElementById("organization").value,
                "about": document.getElementById("about").value,
                "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
            },
            async: false,
            success: function (data) {
                answer = data;
            }
        });
        if (answer === "ok") {
            document.getElementById("signin").removeAttribute("hidden");
            document.getElementById("emailTokenDiv").setAttribute("hidden", "true");
            document.getElementById("finish").setAttribute("hidden", "true");
            document.getElementById("hint").innerHTML = "Registration finished! Meow ~~~";
        } else {
            document.getElementById("emailDiv").removeAttribute("hidden");
            document.getElementById("passwordDiv").removeAttribute("hidden");
            document.getElementById("passwordConfirmDiv").removeAttribute("hidden");
            document.getElementById("hrDiv").removeAttribute("hidden");
            document.getElementById("yearDiv").removeAttribute("hidden");
            document.getElementById("loginDiv").removeAttribute("hidden");
            document.getElementById("specDiv").removeAttribute("hidden");
            document.getElementById("emailTokenDiv").setAttribute("hidden", "true");
            document.getElementById("continue").removeAttribute("hidden");
            document.getElementById("finish").setAttribute("hidden", "true");
            document.getElementById("hint").innerHTML = "Step 1 - Account information";
            document.getElementById("emailTypeError").setAttribute("hidden", "true");
            document.getElementById("emptyLogin").setAttribute("hidden", "true");
            if (answer === "False email") {
                document.getElementById("existsEmail").removeAttribute("hidden");
                document.getElementById("email").setAttribute("class", "form-control is-invalid");
            }
            if (answer === "False login") {
                document.getElementById("existsLogin").removeAttribute("hidden");
                document.getElementById("login").setAttribute("class", "form-control is-invalid");
            }
        }
    }
}

function customLoginCheck() {
    if (document.getElementById("customLogin").checked) {
        document.getElementById("login").removeAttribute("disabled");
        document.getElementById("login").value = '';
        customLogin = true;
    } else {
        document.getElementById("login").setAttribute("disabled", "true");
        customLogin = false;
        fillLogin();
    }
}

function fillLogin() {
    let email = document.getElementById("email").value;
    let loginTemp = '';
    for (let i = 0; i < email.length; i++) {
        if (email[i] === '@') {
            break;
        }
        loginTemp += email[i];
    }
    document.getElementById("login").value = loginTemp;
}

function checkLogin() {
    let login = document.getElementById("login").value;
    let loginTemp = '';
    for (let i = 0; i < login.length; i++) {
        if (login[i] === '@') {
            document.getElementById("loginHelp").setAttribute("class", "form-text font-weight-bold text-danger");
            rejectTime = Date.now() + 1000;
            setTimeout(function () {
                if (Date.now() < rejectTime) {
                    return;
                }
                document.getElementById("loginHelp").setAttribute("class", "form-text font-weight-bold text-muted");
            }, 1000);
            break;
        }
        loginTemp += login[i];
    }
    document.getElementById("login").value = loginTemp;
}