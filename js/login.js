function get_hash(s, salt) {
    result = hash(hash(s + salt) + s + salt);
    for (i = 0; i < 1000; i++) {
        result = hash(result + s + salt);
    }
    return result + " " + salt;
}

function login() {
    var username = $("#username").val();
    var password = $("#password").val();
    $.ajax({
        dataType: "json",
        type: "POST",
        url: "data/accounts.json",
        success: function(o) {
            users = Object.keys(o);
            if (username in o) {
                var nonce = o[username]["nonce"];
                var check = o[username]["pass"];
                var salt = check.split(" ")[1];
                var auth = hash(password + nonce);
                var result = get_hash(hash(auth + nonce), salt);
                // Check to protect from length extension attacks
                if (check.length != result.length) {
                    return false;
                }
                var equality = true;
                for (i = 0; i < check.length; i++) {
                    if (! (check.charAt(i) === result.charAt(i))) {
                        equality = false;
                    }
                }
                if (equality) {
                    var series_id = get_base64();
                    var series_token = get_base64();
                    setCookie("series_id", series_id, 30);
                    setCookie("series_token", series_token, 30);
                    post("home.py", {username: username,
                                     series_id: series_id,
                                     series_token: series_token});
                } else {
                    $("#invalidCredentials").html("Username or password incorrect");
                }
            }
        },
    });
}

document.getElementById("regButton").addEventListener("click", function() {
    login();
}, false);
