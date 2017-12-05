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
                var h = hash(password + nonce);
                var check = o[username]["pass"];
                var salt = check.split(" ")[1];
                var result = hash(hash(password + salt) + password + salt);
                for (i = 0; i < 1000; i++){
                    result = hash(result + password + salt);
                }
                result += ' ' + salt;
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
                    console.log("Correct!");
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