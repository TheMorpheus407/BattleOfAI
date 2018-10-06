function validateToken(success_function){
    let my_data = JSON.stringify({
        "userid": parseInt(getCookie("userid")),
        "token": getCookie("token"),
        "session_token": getCookie("session_token")
    });
    let my_url = get_iam_url() + 'api/iam/validateToken';
    $.ajax({url:my_url,
        type:"post",
        data:my_data,
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: success_function
    });
}

function refreshToken() {
    let my_data = JSON.stringify({
        "userid": getCookie("userid"),
        "token": getCookie("token"),
        "session_token": getCookie("session_token")
    });
    let my_url = get_iam_url() + 'api/iam/validateToken';
    $.ajax({url:my_url,
        type:"post",
        data:my_data,
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            remember_me = getCookie("remember_me") === "true";
            if (remember_me) {
                setCookie("userid", data["userid"], 30);
                setCookie("token", data["token"], 30);
                setCookie("session_token", data["session_token"], 30);
                setCookie("remember_me", "true", 30);
            }
            setCookie("userid", data["userid"]);
            setCookie("token", data["token"]);
            setCookie("session_token", data["session_token"]);
        }
    });
}
