from player import kodi
from main.config import Config



def run(metadata_list):

    player_name = Config.PLAYER_NAME

    run = {
        "kodi": kodi.Kodi
    }

    run[player_name](metadata_list).run()