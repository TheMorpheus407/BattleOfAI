$(document).ready(function () {
    let my_data = JSON.stringify({
        "userid": parseInt(getCookie("userid")),
        "token": getCookie("token"),
        "session_token": getCookie("session_token")
    });
    $.ajax({url:get_iam_url() + 'api/iam/getUserByID/' + getCookie("userid"),
        type:"post",
        data:my_data,
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            document.getElementById('username').value = data['username'];
            document.getElementById('username').innerHTML = data['username'];
            document.getElementById('email').value = data['email'];
            if (data['newsletter']){
                document.getElementById('newsletter').checked = true;
            }
            else {
                document.getElementById('newsletter').checked = false;
            }
        }
    });
});

$("#save_changes").click(function () {

    let form_data = document.getElementById("boai_iam_user_form");
    let my_data = {
        'token': {
            "userid": parseInt(getCookie("userid")),
            "token": getCookie("token"),
            "session_token": getCookie("session_token")
        },
        'old_password': form_data["oldpass"]["value"],
        'newsletter': form_data["newsletter"].checked
    };
    if (form_data["email"]["value"] !== ""){
        my_data.email = form_data["email"]["value"];
    }
    if (form_data["newpass"]["value"] !== ""){
        my_data.new_password = form_data["newpass"]["value"];
    }
    if (form_data["newpass2"]["value"] !== ""){
        my_data.new_password2 = form_data["newpass2"]["value"];
    }
    my_data = JSON.stringify(my_data);
    let my_url = get_iam_url() + 'api/iam/updateUser';
    $.ajax({url:my_url,
        type:"post",
        data:my_data,
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
        
            if (data["success"]){
               alert('Great, the data has been changed!');
            }
            else{
              
                alert('An unknown error has occurred.');
            }

        }
    });
});