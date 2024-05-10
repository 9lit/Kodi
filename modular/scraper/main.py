from modular.scraper import tmdb
from main.config import Config



def run(video_info):

    player_name = Config.PLAYER_NAME

    run = {
        "kodi": tmdb.Tmdb
    }

    info = run[player_name](video_info).run()

    return info