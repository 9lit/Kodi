from scraper import tmdb
from main.config import Config



def run(video_info):

    player_name = Config.PLAYER_NAME

    run = {
        "kodi": tmdb.Tmdb
    }

    info = run[player_name](video_info).run()

    if info:
        return info
    else:
        print("没有可供刮削的数据")
        exit()