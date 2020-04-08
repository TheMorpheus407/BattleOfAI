function display_all_my_games(userid) {
    let my_url = get_games_url() + 'api/games/?user_ids=' + userid;
    $.ajax({
        url: my_url,
        type: "get",
        contentType: "application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            display_games(data.games.map(x => x.id));
        }
    });
}

function display_games(game_ids) {
    game_ids.slice(0, 10).forEach(display_game)
}

function display_game(game_id) {
    let my_url = get_games_url() + 'api/games/' + game_id;
    $.ajax({url:my_url,
        type:"get",
        contentType:"application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {

           game_text = "<li class='game'><span class='time'>"+ data['id'] + "</span><span class='title'>"+ data['game_name'] + "</span><span class='icon'> <a href='game.html?id="+ data['id'] + "' class='flag'><i class='fa fa-play-circle'></i></a></span></li>";
                       
            $("#gamelist").append(game_text);
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
            let gameName = data["game_name"].toLowerCase()
            let elem = document.getElementById(gameName + "-stats");
            if(data["winning_player"] == null || data["winning_player"] === -1){

            }
            else if(data["players"][data["winning_player"]]["id"] === parseInt(getCookie("userid"))){
                elem.dataset.wins = parseInt(elem.dataset.wins) + 1;
                window.pies[gameName].data.datasets[0].data[0] = elem.dataset.wins;
                window.pies[gameName].update();
            }
            else{
                elem.dataset.losses = parseInt(elem.dataset.losses) + 1;
                window.pies[gameName].data.datasets[0].data[1] = elem.dataset.losses;
                window.pies[gameName].update();
            }
        }
    });
}
