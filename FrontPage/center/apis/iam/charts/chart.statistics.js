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

    window.pies = {
        "core": new Chart(
            document.getElementById("chart-area-core").getContext("2d"),
            createConfig(document.getElementById("core-stats"))
        ),
        "abalone": new Chart(
            document.getElementById("chart-area-abalone").getContext("2d"),
            createConfig(document.getElementById("abalone-stats"))
        )
    };
});

function createConfig(statsEl) {
    return config = {
        type: 'pie',
        data: {
            datasets: [{
                data: [statsEl.getAttribute("data-wins"),
                statsEl.getAttribute("data-losses")],
                backgroundColor: [window.chartColors.green,
                window.chartColors.red],
                label: statsEl.getAttribute("data-username")
            }],
            labels: [
                "wins", "losses"
            ]
        },
        options: {
            responsive: true,
            title: { text: statsEl.getAttribute("data-username"), display: true }
        }
    };
}