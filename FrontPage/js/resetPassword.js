$("#resetPasswordTrigger").leanModal({
    top: 100,
    overlay: 0.6,
    closeButton: ".modalClose"
});
$(function () {
    $("#resetPasswordTrigger").click(function () {
        $(".resetPassword").show();
        return false;
    });
});
$("#resetPasswordButton").click(function () {
    let myForm = document.getElementById("resetPasswordForm");
    var params = window.location.search.substr(1).split("&")[0].split("=");
    if (params[0] != "email_token") {
        return;
    }
    email_token = params[1];
    let my_data = JSON.stringify({
        "email_token": email_token,
        "new_password": myForm["new_password"]["value"]
    });
    let my_url = get_iam_url() + 'api/iam/resetPassword';
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
            document.getElementById("resetPasswordDiv").appendChild(node);
        }
    });
});