
$(document).ready(function () {
  
    $(document).ready(function () {

        if (document.cookie.indexOf("token=") <= 0) {
              
            window.location.href='../login.html';
          }


        if(getCookie("token")){
            validateToken(function (data, status, xhr) {
                if(data["success"] == false){
                    
                    window.location.href='../login.html';
                }
            });
        }
    });
});