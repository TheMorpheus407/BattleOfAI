
    window.setTimeout(function(){



        eraseCookie("userid");
        eraseCookie("token");
        eraseCookie("session_token");
        // Move to a new location or you can do something else
        window.location.href = "../index.html";

    }, 1500);
