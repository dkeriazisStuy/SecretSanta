function register() {
    if (! (validateUser() && emailCheck() && passCheck() && passMatchCheck())) {
        return
    }
    var username = $("#username").val();
    var email = $("#email").val();
    var password = $("#password").val();
    $.post({
        url: "signup.py",
        data: "foobar",
    });
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

function emailCheck() {
    var email = $("#email").val();
    if (email.indexOf("@") == -1) {
        $("#invalidEmail").html("Invalid email address");
         return false;
    } else {
        $("#invalidEmail").html("");
        return true;
    }
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
    user_exists($("#username").val(), function(){}, register);
}, false);
