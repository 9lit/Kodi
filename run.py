from main.config import Config
from scraper.tmdb import Tmdb
from player.kodi import Kodi
from main.file import File

import json

class ScrapeInfo():

    def __init__(self) -> None:

        self.player_name = Config.PLAYER_NAME
        self.scraper_name = Config.SCRAPER_NAME

        self.path = Config.PATH
        self.template_episode = Config.TEMPLATE_EPISODE
        self.scraper_all = Config.SCRAPER_ALL

    def scraper(self):
        
        run = {
            "tmdb" : Tmdb
        }
        self.matedata = run[self.scraper_name](video_info=self.info).run()

    def player(self):
        
        run = {
            "kodi": Kodi
        }

        run[self.player_name](self.matedata).run()


    def file(self):

        self.info = File().run()


    def run(self):
        
        self.file()
        if not self.info:
            print(f"[INFO]{self.path}, 此路径下没有需要刮削的文件")
        else:
            print(json.dumps(self.info, ensure_ascii=False, sort_keys=True, indent=2, separators=(",", ":")))
        self.scraper()
        if not self.matedata:
            print(f"{self.scraper_name}.[INFO] 没有可供刮削的数据")
            exit()
        else:
            for name in self.matedata['episode']:
                print(name)
                
        self.player()
            
s = ScrapeInfo().run()
            
                
        
                    



