import requests
import os
from main.config import Config
from main.tools import read_file, write_file
                    
class Tmdb():

    def __init__(self, video_info) -> None:
        
        authorization = Config.AUTHORIZATION
        self.language = Config.LANGUAGE
        self.episode_parseinfo = video_info['episode']
        self.seasons_parseinfo = video_info['season']
        self.thumb_image_url = Config.THUMB_IMAGE_URL
        self.download_image = Config.DOWNLOAD_IMAGE
        self.pid = Config.TMDB_CACHE

        self.urltemplate = {
            self.tv.__name__: "https://api.themoviedb.org/3/search/tv?query={name}&language={language}&year={year}",
            self.episodes.__name__: "https://api.themoviedb.org/3/tv/{id}/season/{season}/episode/{episode}?language={language}",
            self.seasons.__name__: "https://api.themoviedb.org/3/tv/{id}/season/{season}?language={language}"
        }            
        
        
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer %s" % authorization
        }

        self.name = __name__


    def run(self):
        
        self.tvid = {}
        self.seasons_response = []
        self.episodes_response = {}


        # 刮削数据
        if self.seasons_parseinfo and False:
            self.seasons(seasons_parseinfo)

        if self.episode_parseinfo:
            self.episodes()

        # 返回数据
        if self.seasons_response or self.episodes_response:
            response = {
                "tv": None,
                "season": self.seasons_response,
                "episode": self.episodes_response
            }
            # print(json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2, separators=(",", ":")))
            return response


    def tv(self, name, year):
        url = self.urltemplate[self.tv.__name__]
        url = url.format(name=name, year=year, language=self.language)
        self.tv_response = requests.get(url=url, headers=self.headers).json()
        # self.tv_response response.json()['results'][0]['id']

    def seasons(self, seasons_parseinfo):
        
        for season in seasons_parseinfo:
            name, year, season = season
            self.get_tvid(name=name, year=year)
            
            url = self.urltemplate[self.seasons.__name__]
            url= url.format(id=self.id, season=season, language=self.language)
            response = requests.get(url=url, headers=self.headers).json()
            self.seasons_response.append(response)
        
    def episodes(self):
        
        def request(url, headers=True):
            i = 0
            while i < 3:
                if headers:
                    res = requests.get(url=url, headers=self.headers)
                else:
                    res = requests.get(url=url)
                if res.status_code == 200:
                    print(f"{__file__}成功-数据刮削成功 {url}")
                    return res
                else:
                    print(f"失败- 数据刮削失败, 已重试 {i+1} 次, 请检查网络或者 url {url}")
                    i += 1
            return False

        for title, values in self.episode_parseinfo.items():
            
            year = values['year']
            name = values['name']
            self.episodes_response[name] = {
                "nfo": [],
                "jpg": [],
                "outpath": []
            }
            for season_and_episode in values['season_and_episode']:
                season, episode, outpath = season_and_episode

                self.get_tvid(name=name, year=year)
                
                # 获取 tmdb 集数据
                url = self.urltemplate[self.episodes.__name__]
                url = url.format(id=self.id, season=season, episode=episode, language=self.language)

                response = request(url).json()

                if not response:
                    continue
                
                self.episodes_response[name]['nfo'].append(response)
                self.episodes_response[name]['outpath'].append(outpath)
                
                if self.download_image:
                    url = self.thumb_image_url + response['still_path']
                    raw = request(url)
                    if raw:
                        self.episodes_response[name]['jpg'].append(raw)
                    else:
                        self.episodes_response[name]['jpg'].append(None)


    def get_tvid(self, name, year):
        # 获取 tv id

        url = self.urltemplate[self.tv.__name__]
        url = url.format(name=name, language=self.language, year=year)
        key = "%s%s" % (name, year)             

        try:
            self.id = read_file.json(self.pid)[key]
            print(f"成功读取缓存中的 {key}-{self.id}")
        except (TypeError, KeyError):
            self.tv(name, year)
            self.id = self.tv_response['results'][0]['id']
            write_file.txt(self.pid, content=f"{key}-{self.id}", kind="a")
            print(f"{key}的 tv id{self.id} 写入成功..")