$(document).ready(function () {
    try {
        var params = window.location.search.substr(1).split("&")[0].split("=");
        if (params[0] != "email_token") {
            return;
        }
        my_url = get_iam_url() + "api/iam/verifyEmail";
        my_data = JSON.stringify({
            "email_token": params[1]
        });
        $.ajax({url:my_url,
            type:"post",
            data:my_data,
            contentType:"application/json; charset=utf-8",
            cache: false,
            success: function (data, status, xhr) {
                var node = document.createElement("DIV");
                if (data["success"]){
                    document.getElementById("message").style.display = "none";
                    var main_node = document.getElementById("message");
                    var textnode = document.createTextNode(data["message"] + " You will be redirected to the login page in 3 seconds.");
                    main_node.appendChild(textnode);
                    setTimeout(function () {
                        window.location = window.location.protocol + "//" + window.location.host + "/index.html";
                    }, 3000);
                }
            }
        });
    }
    catch (e) {

    }

});