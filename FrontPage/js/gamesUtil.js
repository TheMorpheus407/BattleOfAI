function display_all_my_games(userid) {
    let my_url = get_games_url() + 'api/games/?user_ids='+userid;
    $.ajax({url:my_url,
        type:"get",
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            display_all_games(data);
        }
    });
}
function display_all_games(data) {
    for (let i = 0; i < data["games"].length; i++){
        display_game(data["games"][i]["id"]);
    }
}

function display_game(game_id) {
    let my_url = get_games_url() + 'api/games/' + game_id;
    $.ajax({url:my_url,
        type:"get",
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            game_text = "<a href='game.html?id="+ data['id'] + "' class='collection-item waves-effect waves-red'><i class='small material-icons'>";
            if(data["winning_player"] == null || data["winning_player"] === -1){
                game_text += "sentiment_neutral";
            }
            else if(data["players"][data["winning_player"]]["id"] === parseInt(getCookie("userid"))){
                game_text += "sentiment_very_satisfied";
            }
            else{
                game_text += "sentiment_very_dissatisfied";
            }
            game_text += "</i><span class='space-left' style='text-transform: capitalize'> &nbsp" + data["id"] + "</span><i class='small material-icons red-text secondary-content'>send</i></a>";
            $("#allgames").append(game_text);
        }
    });
}

function display_my_stats(userid){
    let my_url = get_games_url() + 'api/games/?user_ids='+userid;
    $.ajax({url:my_url,
        type:"get",
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            display_stats(data);
        }
    });
}
function display_stats(data) {
    for (let i = 0; i < data["games"].length; i++){
        update_stat(data["games"][i]["id"]);
    }
}

function update_stat(game_id) {
    let my_url = get_games_url() + 'api/games/' + game_id;
    $.ajax({url:my_url,
        type:"get",
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            let elem = document.getElementById("core-stats");
            if(data["winning_player"] == null || data["winning_player"] === -1){

            }
            else if(data["players"][data["winning_player"]]["id"] === parseInt(getCookie("userid"))){
                elem.dataset.wins = parseInt(elem.dataset.wins) + 1;
                window.myPie.data.datasets[0].data[0] = elem.dataset.wins;
                window.myPie.update();
            }
            else{
                elem.dataset.losses = parseInt(elem.dataset.losses) + 1;
                window.myPie.data.datasets[0].data[1] = elem.dataset.losses;
                window.myPie.update();
            }
        }
    });
}