$(function () {
    $("#TODO").click(function () {
        let myForm = document.getElementById("changeUserForm");
        let email = myForm["email"]["value"];
        let oldpass = myForm["oldpass"]["value"];
        let newpass = myForm["newpass"]["value"];
        let newpass2 = myForm["newpass2"]["value"];
        let ok = true;
        if(newpass2 != newpass){
            myForm["newpass2"].style.background = "rgba(255,0,0,0.4)";
            ok = false
        }
        else{
            myForm["newpass2"].style.background = "rgba(0,255,0,0.4)";
        }
        if(newpass.length > 0 && !/^(?=.*[0-9])(?=.*[!@#_:;.,$%&^*])([a-zA-Z0-9!@#_:;.,$%&^*]){6,20}$/.test(newpass)){
            myForm["newpass"].style.background = "rgba(255,0,0,0.4)";
            ok = false;
        }
        else{
            myForm["newpass"].style.background = "rgba(0,255,0,0.4)";
        }
        if(email.length > 0 && !/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,50})$/i.test(email)){
            myForm["email"].style.background = "rgba(255,0,0,0.4)";
            ok = false;
        }
        else{
            myForm["email"].style.background = "rgba(0,255,0,0.4)";
        }
        if(ok) {
            myForm.submit();
        }
        return false;
    });


    $(".button-collapse").sideNav();
    window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };
    var x = document.getElementById("core-stats");
    var config = {
        type: 'pie',
        data: {
            datasets: [{
                data: [x.getAttribute("data-wins"),
                x.getAttribute("data-losses")],
                backgroundColor: [window.chartColors.green,
                window.chartColors.red],
                label: x.getAttribute("data-username")
            }],
            labels: [
                "wins", "losses"
            ]
        },
        options: {
            responsive: true,
            title: {text: x.getAttribute("data-username"),display: true}
        }
    };
    var canvas = document.getElementById("chart-area").getContext("2d");
    var chart = new Chart(canvas, config);
    window.myPie = chart;
});