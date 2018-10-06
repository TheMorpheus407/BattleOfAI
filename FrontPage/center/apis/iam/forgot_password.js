
    $("#send_mail").click(function () {
        let forgotpassword_form_data = document.getElementById("forgotPasswordForm");
        let json_forgotpassword_data = JSON.stringify({"email": forgotpassword_form_data["email"]["value"]});
        let api_url = get_iam_url() + 'api/iam/forgotPassword';
        $.ajax({url:api_url,
            type:"post",
            data:json_forgotpassword_data,
            contentType:"application/json; charset=utf-8",
            cache: false,
            success: function (data, status, xhr) {

                window.location.href="checkmail.html";

            }
        });
    });

$("#set_password").click(function () {
    let form_data = document.getElementById("boai_iam_user_form");
    var params = window.location.search.substr(1).split("&")[0].split("=");
    if (params[0] != "email_token") {
        return;
    }
    email_token = params[1];
    let json_forgotpassword_data = JSON.stringify({
        "email_token": email_token,
        "new_password": form_data["new_password"]["value"]
    });
    let api_url = get_iam_url() + 'api/iam/resetPassword';
    $.ajax({url:api_url,
        type:"post",
        data:json_forgotpassword_data,
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            if (data["success"] == true){
             
                window.location.href='finish.html';
            }else{
             
                window.location.href='failed.html';
            }
    
        }
    });
});