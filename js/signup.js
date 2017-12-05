function get_nonce() {
    var chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~";
    var nonce = "";
    for (i = 0; i < 16; i++) {
        nonce += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return nonce
}

function register() {
    if (! (validateUser() && emailCheck() && passCheck() && passMatchCheck())) {
        return
    }
    var username = $("#username").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var nonce = get_nonce();
    var h = hash(password + nonce);
    var series_id = get_nonce();
    var token = get_nonce();
    setCookie("series_id", series_id, 30);
    setCookie("token", token, 30);
    post("signup.py", {username: username,
                       email: email,
                       key: h,
                       nonce: nonce,
                       series_id: series_id,
                       token: token});
}

function user_exists(user, f_success, f_fail) {
    return $.ajax({
        dataType: "json",
        type: "POST",
        url: "data/accounts.json",
        success: function(o) {
            if (user in o) {
                f_success();
            } else {
                f_fail();
            }
        },
    });
}

function email_exists(email, f_success, f_fail) {
    return $.ajax({
        dataType: "json",
        type: "POST",
        url: "data/accounts.json",
        success: function(o) {
            users = Object.keys(o);
            exists = false;
            for (i = 0; i < users.length; i++) {
                if (email === o[users[i]]['email']) {
                    exists = true;
                    break;
                }
            }
            if (exists) {
                f_success();
            } else {
                f_fail();
            }
        },
    });
}

function validateUser() {
    var username = $("#username").val();
    if (! /^[a-zA-Z0-9_-]*$/.test(username)) {
        $("#invalidUsername").html("Username may only contain ascii letters, numbers, underscores (_), and hyphens (-)");
        return false;
    } else {
        $("#invalidUsername").html("");
        return true;
    }
}

function usernameCheck() {
    var username = $("#username").val();
    var success = function() {
        $("#invalidUsername").html("Username is already taken");
        return false;
    }
    return user_exists(username, success, validateUser);
}

function validateEmail() {
    var email = $("#email").val();
    if (email.indexOf("@") == -1) {
        $("#invalidEmail").html("Invalid email address");
         return false;
    } else {
        $("#invalidEmail").html("");
        return true;
    }
}

function emailCheck() {
    var email = $("#email").val();
    var success = function() {
        $("#invalidEmail").html("Email is already taken");
        return false;
    }
    return email_exists(email, success, validateEmail);
}

function passCheck() {
    var password = $("#password").val();
    if (password.length < 6) {
        $("#invalidPass").html("Password should be at least 6 characters");
        return false;
    } else {
        $("#invalidPass").html("");
        return true;
    }
}

function passMatchCheck() {
    var password = $("#password").val();
    var confirmPassword = $("#password_confirm").val();
    if (password != confirmPassword) {
        $("#passUnmatched").html("Passwords do not match!");
        return false;
    } else {
        $("#passUnmatched").html("");
        return true;
    }
}

$(document).ready(function () {
    $("#username").keyup(usernameCheck);
});

$(document).ready(function () {
    $("#email").keyup(emailCheck);
});

$(document).ready(function () {
   $("#password").keyup(passCheck);
});

$(document).ready(function () {
   $("#password, #password_confirm").keyup(passMatchCheck);
});

document.getElementById("regButton").addEventListener("click", function() {
    user_exists($("#username").val(), function(){},
        function(){email_exists($("#email").val(), function(){}, register)});
}, false);
