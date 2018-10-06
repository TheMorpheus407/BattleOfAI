function loggedIn(){

    
}
$(document).ready(function () {
  
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

    $("#do_login").click(function () {
        
        if(getCookie("cookieconsent_status") == null){
            alert("You have to accept cookies first!");
            return;
        }
        let login_form_data = document.getElementById("boai_iam_user_form");
        let entered_user_name =  login_form_data["username"]["value"];
        let entered_password = login_form_data["password"]["value"];
        
        let json_login_data =   JSON.stringify(   {"username": entered_user_name,
                                                   "password": entered_password} );
    
        let api_url = get_iam_url() + 'api/iam/login';

        $.ajax({url:api_url,
            type:"post",
            data:json_login_data,
            contentType:"application/json; charset=utf-8",
            cache: false,
            success: function (data, status, xhr) {
        
                if (data["userid"] !== null) {

                    setCookie("userid", data["userid"]);
                    setCookie("token", data["token"]);
                    setCookie("session_token", data["session_token"]);
                    window.location.href="center/home.html";

                }
                else {

                    document.getElementById("error_case").innerHTML = "These login credentials are incorrect!"
                
                } 
            }
        });
        return false;
    });

});