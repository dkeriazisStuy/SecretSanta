function create_group() {
    var group_name = $("#name").val();
    var group_description = $("#description").val();
    f_success = function(username, series_id, new_token) {
        post("home.py", {username: username,
                         series_id: series_id,
                         series_token: new_token,
                         group_name: group_name,
                         group_description: group_description});
    }
    f_fail = function() {
        window.location = "main.html";
    }
    checkCookies(f_success, f_fail);
}

document.getElementById("addGroup").addEventListener("click", function() {
    create_group();
}, false);
