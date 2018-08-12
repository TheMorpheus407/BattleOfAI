import unittest
import requests

url = "http://0.0.0.0:1337/api/"
username = "Challo"
passw = "asdf1234"
resp = requests.post("http://0.0.0.0:1338/api/iam/login", json={"username": username, "password": passw})
user_0_key = str([resp.json()["token"], resp.json()["session_token"]])
user_id = resp.json()["userid"]


class GamesTest(unittest.TestCase):
    def test_game_state(self):
        for state in ["WAITING", "FINISHED", "ABORTED", "STARTED"]:
            resp = requests.get(url + "games/?game_state=" + state)
            games = resp.json()['games']
            for i in games:
                id = i['id']
                resp2 = requests.get(url+"games/"+ str(id))
                self.assertEqual(resp2.json()['game_state'], state)

    def test_user_ids(self):
        for id in ["1", "0", "1_0", "0_1"]:
            resp = requests.get(url + "games/?user_ids=" + id)
            games = resp.json()['games']
            for i in games:
                game_id = i['id']
                resp2 = requests.get(url+"games/"+ str(game_id))
                for player_id in id.split("_"):
                    found = False
                    for game_player in resp2.json()['players']:
                        if int(player_id) ==  game_player['id']:
                            found = True
                    self.assertEqual(found, True)

    def test_game_name(self):
        for name in ["Interface"]:
            resp = requests.get(url + "games/?game_name=" + name)
            games = resp.json()['games']
            for i in games:
                id = i['id']
                resp2 = requests.get(url+"games/"+ str(id))
                self.assertEqual(resp2.json()['game_name'], name)

class InterfaceRegisterTest(unittest.TestCase):
    def setUp(self):
        self.game_id = int(requests.post(url + "games/createGame", json={"game_name": "Interface"}).text)
        self.game_url = url + "games/" + str(self.game_id)

    def test_register(self):
        resp = requests.post(self.game_url + "/registerPlayer", json={"id": user_id, "token": user_0_key})
        self.assertIn("true", resp.text)
        game_info = requests.get(self.game_url).json()
        self.assertEqual(game_info["players"][0]['id'], user_id)


class InterfaceRegisteredTest(unittest.TestCase):
    def setUp(self):
        self.game_id = int(requests.post(url + "games/createGame", json={"game_name": "Interface"}).text)
        self.game_url = url + "games/" + str(self.game_id)
        resp = requests.post(self.game_url + "/registerPlayer", json={"id": user_id, "token": user_0_key})
        self.assertIn("true", resp.text)
        resp = requests.post(self.game_url + "/registerPlayer", json={"id": user_id, "token": user_0_key})
        self.assertIn("true", resp.text)
        self.game_info = requests.get(self.game_url).json()

    def test_slots_available(self):
        self.assertEqual(self.game_info["open_slots"], 0)

    def test_players_registered(self):
        for i in self.game_info["players"]:
            self.assertEqual(i['id'], user_id)

    def test_game_state(self):
        self.assertEqual(self.game_info["game_state"], "STARTED")

    def test_playing(self):
        data = {"player": {"id": user_id, "token": user_0_key}, "turn": "[]"}
        for i in range(9):
            resp = requests.post(self.game_url + "/makeTurn", json=data).text
            self.assertIn("true", resp)
        resp = requests.post(self.game_url + "/makeTurn", json=data).text
        self.assertIn("false", resp)

    def test_bad_moves(self):
        data = {"player": {"id": user_id, "token": user_0_key}, "turn": "[1337]"}
        resp = requests.post(self.game_url + "/makeTurn", json=data).text
        self.assertIn("false", resp)
        game_info = requests.get(self.game_url).json()
        self.assertEqual(game_info["game_state"], "ABORTED")


class InterfacePlayTest(unittest.TestCase):
    def setUp(self):
        self.game_id = int(requests.post(url + "games/createGame", json={"game_name": "Interface"}).text)
        self.game_url = url + "games/" + str(self.game_id)
        resp = requests.post(self.game_url + "/registerPlayer", json={"id": user_id, "token": user_0_key})
        resp = requests.post(self.game_url + "/registerPlayer", json={"id": user_id, "token": user_0_key})
        data = {"player": {"id": user_id, "token": user_0_key}, "turn": "[]"}
        for i in range(10):
            resp = requests.post(self.game_url + "/makeTurn", json=data).text
        self.game_info = requests.get(self.game_url).json()

    def test_game_state(self):
        self.assertEqual(self.game_info["game_state"], "FINISHED")

    def test_move_after_finished(self):
        data = {"player": {"id": user_id, "token": user_0_key}, "turn": "[]"}
        resp = requests.post(self.game_url + "/makeTurn", json=data).status_code
        self.assertEqual(resp, 403)

if __name__ == '__main__':
    unittest.main()