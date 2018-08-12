import json

save_folder = 'Games_Archive/'

def write_to_file(id, game_instance):
    my_json = {
        'id': id,
        'active_player': game_instance.active_player,
        'history': game_instance.history
    }
    file_name = save_folder + str(id) + ".json"
    with open(file_name, 'w') as outfile:
        json.dump(my_json, outfile)
    return True