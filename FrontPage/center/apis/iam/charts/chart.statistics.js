$(function () {

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