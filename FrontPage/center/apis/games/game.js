$(document).ready(function () {
    var params = window.location.search.substr(1).split("&")[0].split("=");
    if (params[0] != "id") {
        return;
    }
    my_url = get_games_url() + "api/games/" + params[1];
    $.ajax({
        url: my_url,
        type: "get",
        contentType: "application/json; charset=utf-8",
        cache: false,
        success: function (data, status, xhr) {
            if(data["game_name"] === "Core"){
                display_core_game(data);
            }
        }
    });
});

function display_core_game(data) {
    let core_div = document.getElementById("core");
    let element_template = `
    <table id="core-MOVEID" style="display: none" class="table table-bordered">
    <colgroup>
    <col width="25">
    <col width="25">
    <col width="25">
  </colgroup>
                <thead>
                <tr>
                    <th>1</th>
                    <th>2</th>
                    <th>3</th>
                    <th>4</th>
                    <th>5</th>
                    <th>6</th>
                    <th>7</th>
                    <th>8</th>
                </tr>
                </thead>
                <tbody id="core-game-content">
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                <tr>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                    <td>#</td>
                </tr>
                </tbody>
            </table>
    `;
    let newelement = "";
    if (parseInt(getCookie("userid")) === data["players"][0]["id"]){
        var white = "<div style='width: 25px; height: 25px; background-color: white; border-radius: 25px; border: 1px solid red'></div>";
        var black = "<div style='width: 25px; height: 25px; background-color: black; border-radius: 25px; border: 1px solid white'></div>";
    }
    if (parseInt(getCookie("userid")) === data["players"][1]["id"]){
        var white = "<div style='width: 25px; height: 25px; background-color: white; border-radius: 25px; border: 1px solid black'></div>";
        var black = "<div style='width: 25px; height: 25px; background-color: black; border-radius: 25px; border: 1px solid red'></div>";
    }
    for (let i = 0; i < data["history"].length; i++){
        newelement = element_template.replace("MOVEID", i+1);
        let board = data["history"][i]["board"];
        for (let x = 0; x < board.length; x++){
            for (let y = 0; y < board[x].length; y++){
                if (board[x][y] === "X"){
                    newelement = newelement.replace("#", white);
                }
                else if(board[x][y] === "O"){
                    newelement = newelement.replace("#", black);
                }
                else {
                    newelement = newelement.replace("#", " ");
                }
            }
        }
        core_div.innerHTML = core_div.innerHTML + newelement;
    }
}
function back() {
    let active = document.getElementsByClassName('active-game')[0];
    let id = parseInt(active.id.substr(5));
    if(id === 0){
        return;
    }
    let new_id = id-1;
    let new_obj = document.getElementById('core-' + new_id);
    active.classList.remove('active-game');
    active.style.display = "none";
    new_obj.style.display = "";
    new_obj.classList.add('active-game');
}
function forward() {
    let active = document.getElementsByClassName('active-game')[0];
    let id = parseInt(active.id.substr(5));
    let new_id = id+1;
    let elem_id = 'core-' + new_id;
    let new_obj = document.getElementById(elem_id);
    if(new_obj == null){
        return;
    }
    active.classList.remove('active-game');
    active.style.display = "none";
    new_obj.style.display = "";
    new_obj.classList.add('active-game');
}