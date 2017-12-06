function get_salt() {
    var chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~";
    var nonce = "";
    for (i = 0; i < 16; i++) {
        nonce += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return nonce
}

function get_base64() {
    var chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_";
    var result = "";
    for (i = 0; i < 16; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

function hash(s) {
    var h = new jsSHA("SHA-512", "TEXT");
    h.update(s);
    return h.getHash("HEX");
}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

function getCookie(name) {
    var name = name + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookies() {
    var series_id = getCookie("series_id");
    var token = getCookie("series_token");
    $.ajax({
        dataType: "json",
        type: "POST",
        url: "data/accounts.json",
        success: function(o) {
            console.log(o)
            var users = Object.keys(o);
            var match = false;
            for (i = 0; i < users.length; i++) {
                if (o[users[i]]["series_id"] == series_id) {
                    console.log("ID Found");
                    console.log(series_id);
                    console.log(token);
                    var username = users[i];
                    if (o[users[i]]["series_token"] == hash(token)) {
                        match = true;
                        var new_token = get_base64(); 
                        setCookie("series_id", series_id, 30);
                        setCookie("series_token", new_token, 30);
                        console.log("Match!");
                        console.log(username);
//                        post("home.py", {username: users[i],
//                                         series_id: series_id,
//                                         series_token: new_token});
                    } else {
                        return false;  // TODO: Implement warnings and cool-down for forged token
                    }
                }
            }
            if (!match) {
                console.log("About to redirect..."); // TODO: Fix async call
                // window.location = "main.html";
            }
        }
    });
}
