import os, re
from main.config import Config

class File():
    
    def __init__(self) -> None:
        self.scraper_all = Config.SCRAPER_ALL
        self.path = Config.PATH

    def run(self):
        self.lack_info()
        return self.matedata


    def get_video_file(self):
        # 获取指定路径下的所有没有元数据的文件
        video_file = {}
        files, dirs = [], []

        for root, dir, file in os.walk(self.path):
            if dir:
                dirs.append(dir)
            
            files.append(file)

        y, i, flag = 1, 0, True
        for dir in dirs:
            if dir:
                if flag:
                    flag = False
                    video_file = {d: {} for d in dir}
                    first_key = dir

                else:
                    video_file[first_key[i]]['tv'] = files[y]
                    y+=1

                    for d in dir:
                        d = re.findall(r'\d+', d)[0]
                        video_file[first_key[i]][d] = files[y]
                        y+=1
                    
                    i += 1
        
        self.video_file = video_file

    def lack_info(self):

        self.get_video_file()

        def tv():
            lack_tvinfo = [names for names, values in self.video_file.items() if 'tvshow.nfo' not in values['tv']]

            return lack_tvinfo

        def season():

            lack_seasoninfo = {}
            for names, values in self.video_file.items():
                for season, value in values.items():
                    if season == 'tv':
                        continue
                    if "season.nfo" not in value:
                        try:
                            lack_seasoninfo[names].append(season)
                        except KeyError:
                            lack_seasoninfo[names] = []
                            lack_seasoninfo[names].append(season)

            return lack_seasoninfo
        
        def episode():
            lack_episodeinfo = {}
            def get_name_and_year(name):
                return name.split(".")[::2]
            
            def get_season_and_episode(title, path):
                return re.findall(r"\d+", title) + [path]

            for names, values in self.video_file.items():
                
                name, year = get_name_and_year(names)

                lack_episodeinfo[names] = {
                    "season_and_episode": [],
                    "name": name,
                    "year": year
                }

                for season, value in values.items():
                    if season == 'tv':
                        continue
                    videos = [i for i in value if os.path.splitext(i)[-1] in [".mkv", ".mp4"]]
                    for video in videos:
                        title, suffix = os.path.splitext(video)
                        if f"{title}-thumb.jpg" not in value or  f"{title}.nfo" not in value:
                            path = os.path.join(self.path, names, f'Season {season}', title)
                            lack_episodeinfo[names]['season_and_episode'].append(get_season_and_episode(title, path))
                if not lack_episodeinfo[names]['season_and_episode']:
                    del lack_episodeinfo[names]
                                
            return lack_episodeinfo

        def run():
            
            lack_episodeinfo = episode()

            metadata = {
                "tv": tv(),
                "season": season(),
                "episode": lack_episodeinfo,
            }
            
            return metadata


        self.matedata = run()
