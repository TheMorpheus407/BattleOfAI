function loggedIn(){

    
}


$(document).ready(function () {
    try {
        var params = window.location.search.substr(1).split("&")[0].split("=");
        if (params[0] != "email_token") {
            return;
        }
        api_url = get_iam_url() + "api/iam/verifyEmail";
        json_data = JSON.stringify({
            "email_token": params[1]
        });

        $.ajax({url:api_url,
            type:"post",
            data:json_data,
            contentType:"application/json; charset=utf-8",
            cache: false,
            success: function (data, status, xhr) {
              
                if (data["success"]) {
                    document.getElementById("verifyemail_message_heading").innerHTML = "Your account is ready!";
                    document.getElementById("verifyemail_message_description").innerHTML = "The registration is complete, your account can be used immediately.";
                }
            }
        });
    }
    catch (e) {

    }

});


$(function () {

    $("#do_signup").click(function () {
        let signup_form_data = document.getElementById("boai_iam_user_form");
        let username = signup_form_data["username"]["value"];
        let email = signup_form_data["email"]["value"];
        let password = signup_form_data["password"]["value"];
        let trouble = false;
      
        if (!/^([0-9a-zA-Z._]){3,30}/.test(username)) {
            trouble = true;
        }

        if(!/^(?=.*[0-9])(?=.*[!@#_:;.,$%&^*])([a-zA-Z0-9!@#_:;.,$%&^*]){6,20}$/.test(password)){
            trouble = true;
        }
    
        if(!/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,50})$/i.test(email)){
            trouble = true;
        }

        if(trouble === false) {
            let json_signup_data = JSON.stringify({  "username": username,
                                            "email": email,
                                            "password": password,
                                            "newsletter": signup_form_data["sendUpdates"].checked});
                                
         let api_url = get_iam_url() + 'api/iam/register';


            $.ajax({url:api_url,
                type:"post",
                data:json_signup_data,
                contentType:"application/json; charset=utf-8",
                cache: false,
                success: function (data, status, xhr) {
                
                    if (data["success"] == true){
                        window.location.href="finishsignup.html";
                     }
                     else
                     {
                         document.getElementById("error_case").innerHTML = "There is a problem with your entered data. "
                    }   
                }
            });
        }
        return false;
    });

});