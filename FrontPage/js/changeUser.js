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

function change_user_submit() {
    let myForm = document.getElementById("changeUserForm");
    let my_data = {
        'token': {
            "userid": parseInt(getCookie("userid")),
            "token": getCookie("token"),
            "session_token": getCookie("session_token")
        },
        'old_password': myForm["oldpass"]["value"],
        'newsletter': myForm["newsletter"].checked
    };
    if (myForm["email"]["value"] !== ""){
        my_data.email = myForm["email"]["value"];
    }
    if (myForm["newpass"]["value"] !== ""){
        my_data.new_password = myForm["newpass"]["value"];
    }
    if (myForm["newpass2"]["value"] !== ""){
        my_data.new_password2 = myForm["newpass2"]["value"];
    }
    my_data = JSON.stringify(my_data);
    let my_url = get_iam_url() + 'api/iam/updateUser';
    $.ajax({url:my_url,
        type:"post",
        data:my_data,
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            let elem = document.getElementById('message');
            elem.style.display = "inline";
            if (data["success"]){
                elem.classList.add('green-text');
            }
            else{
                elem.classList.add('red-text');
            }
            elem.innerText = data["message"];
        }
    });
}