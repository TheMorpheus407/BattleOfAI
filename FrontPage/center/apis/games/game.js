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
            let gameViewerHeading = document.getElementById('game-viewer-heading')
            gameViewerHeading.innerHTML = data["game_name"] + " " + gameViewerHeading.innerHTML

            switch (data["game_name"]) {
                case "Core":
                    display_core_game(data);
                    break;
                case "Abalone":
                    display_abalone_game(data);
                    break;
            }
        }
    });
});

function display_core_game(data) {
    document.getElementById("game-container").style.width = "410px";
    let core_div = document.getElementById("game");
    core_div.innerHTML = `
<table class="table table-bordered active-game"  id="core-0">
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
    <tbody id='core-game-content'>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr></tr>
    </tbody>
</table>
    `
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
    if (parseInt(getCookie("userid")) === data["players"][0]["id"]) {
        var white = "<div style='width: 25px; height: 25px; background-color: white; border-radius: 25px; border: 1px solid red'></div>";
        var black = "<div style='width: 25px; height: 25px; background-color: black; border-radius: 25px; border: 1px solid white'></div>";
    }
    if (parseInt(getCookie("userid")) === data["players"][1]["id"]) {
        var white = "<div style='width: 25px; height: 25px; background-color: white; border-radius: 25px; border: 1px solid black'></div>";
        var black = "<div style='width: 25px; height: 25px; background-color: black; border-radius: 25px; border: 1px solid red'></div>";
    }
    for (let i = 0; i < data["history"].length; i++) {
        newelement = element_template.replace("MOVEID", i + 1);
        let board = data["history"][i]["board"];
        for (let x = 0; x < board.length; x++) {
            for (let y = 0; y < board[x].length; y++) {
                if (board[x][y] === "X") {
                    newelement = newelement.replace("#", white);
                }
                else if (board[x][y] === "O") {
                    newelement = newelement.replace("#", black);
                }
                else {
                    newelement = newelement.replace("#", " ");
                }
            }
        }
        core_div.innerHTML = core_div.innerHTML + newelement;
    }
    document.getElementById("btn-back").addEventListener("click", core_back);
    document.getElementById("btn-forward").addEventListener("click", core_forward);
}

function core_back() {
    let active = document.getElementsByClassName('active-game')[0];
    let id = parseInt(active.id.substr(5));
    if (id === 0) {
        return;
    }
    let new_id = id - 1;
    let new_obj = document.getElementById('core-' + new_id);
    active.classList.remove('active-game');
    active.style.display = "none";
    new_obj.style.display = "";
    new_obj.classList.add('active-game');
}
function core_forward() {
    let active = document.getElementsByClassName('active-game')[0];
    let id = parseInt(active.id.substr(5));
    let new_id = id + 1;
    let elem_id = 'core-' + new_id;
    let new_obj = document.getElementById(elem_id);
    if (new_obj == null) {
        return;
    }
    active.classList.remove('active-game');
    active.style.display = "none";
    new_obj.style.display = "";
    new_obj.classList.add('active-game');
}

function display_abalone_game(data) {
    let link  = document.createElement("link");
    link.rel  = "stylesheet";
    link.type = "text/css";
    link.href = "layout_assets/css/abalone.css";
    document.getElementsByTagName("head")[0].appendChild(link);

    document.getElementById("game").innerHTML = `
<div class="board">
    <div class="space space-a1" title="A1"></div>
    <div class="space space-a2" title="A2"></div>
    <div class="space space-a3" title="A3"></div>
    <div class="space space-a4" title="A4"></div>
    <div class="space space-a5" title="A5"></div>
    <div class="space space-b1" title="B1"></div>
    <div class="space space-b2" title="B2"></div>
    <div class="space space-b3" title="B3"></div>
    <div class="space space-b4" title="B4"></div>
    <div class="space space-b5" title="B5"></div>
    <div class="space space-b6" title="B6"></div>
    <div class="space space-c1" title="C1"></div>
    <div class="space space-c2" title="C2"></div>
    <div class="space space-c3" title="C3"></div>
    <div class="space space-c4" title="C4"></div>
    <div class="space space-c5" title="C5"></div>
    <div class="space space-c6" title="C6"></div>
    <div class="space space-c7" title="C7"></div>
    <div class="space space-d1" title="D1"></div>
    <div class="space space-d2" title="D2"></div>
    <div class="space space-d3" title="D3"></div>
    <div class="space space-d4" title="D4"></div>
    <div class="space space-d5" title="D5"></div>
    <div class="space space-d6" title="D6"></div>
    <div class="space space-d7" title="D7"></div>
    <div class="space space-d8" title="D8"></div>
    <div class="space space-e1" title="E1"></div>
    <div class="space space-e2" title="E2"></div>
    <div class="space space-e3" title="E3"></div>
    <div class="space space-e4" title="E4"></div>
    <div class="space space-e5" title="E5"></div>
    <div class="space space-e6" title="E6"></div>
    <div class="space space-e7" title="E7"></div>
    <div class="space space-e8" title="E8"></div>
    <div class="space space-e9" title="E9"></div>
    <div class="space space-f2" title="F2"></div>
    <div class="space space-f3" title="F3"></div>
    <div class="space space-f4" title="F4"></div>
    <div class="space space-f5" title="F5"></div>
    <div class="space space-f6" title="F6"></div>
    <div class="space space-f7" title="F7"></div>
    <div class="space space-f8" title="F8"></div>
    <div class="space space-f9" title="F9"></div>
    <div class="space space-g3" title="G3"></div>
    <div class="space space-g4" title="G4"></div>
    <div class="space space-g5" title="G5"></div>
    <div class="space space-g6" title="G6"></div>
    <div class="space space-g7" title="G7"></div>
    <div class="space space-g8" title="G8"></div>
    <div class="space space-g9" title="G9"></div>
    <div class="space space-h4" title="H4"></div>
    <div class="space space-h5" title="H5"></div>
    <div class="space space-h6" title="H6"></div>
    <div class="space space-h7" title="H7"></div>
    <div class="space space-h8" title="H8"></div>
    <div class="space space-h9" title="H9"></div>
    <div class="space space-i5" title="I5"></div>
    <div class="space space-i6" title="I6"></div>
    <div class="space space-i7" title="I7"></div>
    <div class="space space-i8" title="I8"></div>
    <div class="space space-i9" title="I9"></div>
</div>
    `;

    const btnBack = document.getElementById("btn-back")
    btnBack.setAttribute("disabled", "disabled")
    const btnForward = document.getElementById("btn-forward");
    let stateIndex = 0;
    update_abalone_board(data["history"][0]["board"]);
    btnBack.addEventListener("click", () => {
        if (stateIndex > 0) {
            update_abalone_board(data["history"][--stateIndex]["board"]);
        }
        if (stateIndex === 0) {
            btnBack.setAttribute("disabled", "disabled")
        }
        btnForward.removeAttribute("disabled")
    });
    btnForward.addEventListener("click", () => {
        if (stateIndex < data["history"].length - 1) {
            update_abalone_board(data["history"][++stateIndex]["board"]);
        }
        if (stateIndex === data["history"].length - 1) {
            btnForward.setAttribute("disabled", "disabled")
        }
        btnBack.removeAttribute("disabled")
    });
}

function update_abalone_board(board) {
    board = board.flat().reverse();
    const spaces = document.getElementsByClassName("space");
    for (let space in spaces) {
        if (spaces[space].classList !== undefined) {
            spaces[space].classList.remove("space-white", "space-black");
            if (board[space] === "BLACK") {
                spaces[space].classList.add("space-black");
            } else if (board[space] === "WHITE") {
                spaces[space].classList.add("space-white");
            }
        }
    }
}
