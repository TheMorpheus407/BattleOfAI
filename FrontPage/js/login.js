function loggedIn(){
    let elements = document.getElementsByClassName("memberLink");
    elements[0].style.display = "inline-block";
    elements[1].style.display = "inline-block";
    let login_elements = document.getElementsByClassName("login-dropdown-menu");
    login_elements[0].style.display = "none";
    login_elements[1].style.display = "none";
}
$(document).ready(function () {
    $(".loginTrigger").leanModal({
        top: 100,
        overlay: 0.6,
        closeButton: ".modalClose"
    });
    $(".registerTrigger").leanModal({
        top: 100,
        overlay: 0.6,
        closeButton: ".modalClose"
    });
    $(".forgotPasswordTrigger").leanModal({
        top: 100,
        overlay: 0.6,
        closeButton: ".modalClose"
    });

    $(document).ready(function () {
        if(getCookie("token")){
            validateToken(function (data, status, xhr) {
                if(data["success"]){
                    loggedIn();
                }
            });
        }
    });
});
$(function () {
    $(".loginTrigger").click(function () {
        $(".userLogin").show();
        $(".forgotPassword").hide();
        $(".userRegister").hide();
        $(".headerTitle").text("Login");
        return false;
    });
    $(".forgotPasswordTrigger").click(function () {
        $(".userLogin").hide();
        $(".forgotPassword").show();
        $(".userRegister").hide();
        $(".headerTitle").text("Reset Password");
        return false;
    });
    $(".forgotPasswordTriggerLink").click(function () {
        $(".userLogin").hide();
        $(".forgotPassword").show();
        $(".userRegister").hide();
        $(".headerTitle").text("Reset Password");
        return false;
    });
    $(".registerTrigger").click(function () {
        $(".userLogin").hide();
        $(".forgotPassword").hide();
        $(".userRegister").show();
        $(".headerTitle").text("Register");
        return false;
    });
    $(".regBtn").click(function () {
        $(".userLogin").hide();
        $(".forgotPassword").hide();
        $(".userRegister").show();
        $(".headerTitle").text("Register");
        return false;
    });
    $(".loginBtn").click(function () {
        $(".userLogin").show();
        $(".forgotPassword").hide();
        $(".userRegister").hide();
        $(".headerTitle").text("Login");
        return false;
    });

    $("#registerUser").click(function () {
        let myForm = document.getElementById("registerForm");
        let username = myForm["username"]["value"];
        let email = myForm["email"]["value"];
        let password = myForm["password"]["value"];
        let ok = true;
        if (!/^([0-9a-zA-Z._]){3,30}/.test(username)) {
            myForm["username"].style.background = "rgba(255,0,0,0.4)";
            ok = false;
        }else{
            myForm["username"].style.background = "rgba(0,255,0,0.4)";
        }
        if(!/^(?=.*[0-9])(?=.*[!@#_:;.,$%&^*])([a-zA-Z0-9!@#_:;.,$%&^*]){6,20}$/.test(password)){
            myForm["password"].style.background = "rgba(255,0,0,0.4)";
            ok = false;
        }else{
            myForm["password"].style.background = "rgba(0,255,0,0.4)";
        }
        if(!/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,50})$/i.test(email)){
            myForm["email"].style.background = "rgba(255,0,0,0.4)";
            ok = false;
        }else{
            myForm["email"].style.background = "rgba(0,255,0,0.4)";
        }
        if(ok) {
            let my_data = JSON.stringify({   "username": username,
                "email": email,
                "password": password,
                "newsletter": myForm["sendUpdates"].checked});
            let my_url = get_iam_url() + 'api/iam/register';
            $.ajax({url:my_url,
                type:"post",
                data:my_data,
                contentType:"application/json; charset=utf-8",
                cache: false,
                success: function (data, status, xhr) {
                    var node = document.createElement("DIV");
                    if (data["success"] == false){
                        node.style.color = '#BB0000';
                    }else{
                        node.style.color = '#0cbb0a';
                    }
                    var textnode = document.createTextNode(data["message"]);
                    node.appendChild(textnode);
                    document.getElementById("userRegisterDiv").appendChild(node);
                }
            });
        }
        return false;
    });

    $("#loginUser").click(function () {
        if(getCookie("cookieconsent_status") == null){
            alert("You have to accept cookies first!");
            return;
        }
        let myForm = document.getElementById("loginForm");
        let my_data = JSON.stringify({"username": myForm["name"]["value"],
            "password": myForm["password"]["value"]});
        let my_url = get_iam_url() + 'api/iam/login';
        let remember_me = myForm["remember"].checked;
        $.ajax({url:my_url,
            type:"post",
            data:my_data,
            contentType:"application/json; charset=utf-8",
            cache: false,
            success: function (data, status, xhr) {
                if (remember_me) {
                    setCookie("userid", data["userid"], 30);
                    setCookie("token", data["token"], 30);
                    setCookie("session_token", data["session_token"], 30);
                    setCookie("remember_me", "true", 30);
                }
                setCookie("userid", data["userid"]);
                setCookie("token", data["token"]);
                setCookie("session_token", data["session_token"]);
                loggedIn();
                window.location = window.location.protocol + "//" + window.location.host + "/members.html";
            }
        });
        return false;
    });

    $("#forgotPasswordButton").click(function () {
        let myForm = document.getElementById("forgotPasswordForm");
        let my_data = JSON.stringify({"email": myForm["email"]["value"]});
        let my_url = get_iam_url() + 'api/iam/forgotPassword';
        $.ajax({url:my_url,
            type:"post",
            data:my_data,
            contentType:"application/json; charset=utf-8",
            cache: false,
            success: function (data, status, xhr) {
                var node = document.createElement("DIV");
                var textnode = document.createTextNode("If there is an account with the email you provided, a mail has been sent to you.");
                node.appendChild(textnode);
                document.getElementById("forgotPasswordDiv").appendChild(node);
            }
        });
    });
    $("#contactFormSendButton").click(function () {
        window.alert("This functionality is not yet implemented. Please contact the admin via social media or write a mail to kontakt@the-morpheus.de .");
    });

});
