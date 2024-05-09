import os
from main.tools import read_file

now_path = os.path.dirname(__file__)
home_dir, filename = os.path.split(now_path)

path = "config.yml"
path = os.path.join(home_dir, path)

class Config:

    config = read_file.yaml(path)
    
    HOME = home_dir
    PLAYER_NAME = config['default_template']
    SCRAPER_NAME = config['default_scraper']

    # 播放器的配置文件     
    template_player = config['template'][PLAYER_NAME]
    TEMPLATE_EPISODE =  os.path.join(home_dir, template_player['episode']) 

    # 刮削器的配置
    scraper_config = config[SCRAPER_NAME]
    scraper_url = scraper_config['url']
    auth = os.getenv(scraper_config['evn_auth'])
    confi_auth = scraper_config['authorization']
    if auth or confi_auth:
        AUTHORIZATION = auth if auth else confi_auth
    else:
        print("获取 令牌失败,请检查令牌")
        exit()

    LANGUAGE = scraper_config['language']
    THUMB_IMAGE_URL = scraper_url['thumb_image_url']
    THUMB_PERSON_URL = scraper_url['thumb_person_url']

    # 刮削路径
    path = config['path'].replace("\\", "/").split("/")

    path = os.path.join(*path)
    PATH = path.replace("C:", "C:\\") if "C:\\" not in path else path

    print(PATH)
    
    # 是否刮削全部
    SCRAPER_ALL = config['scraper_all']

    # 是否刮削图片
    DOWNLOAD_IMAGE = config["download_image"]

    TMDB_CACHE = os.path.join(HOME, "tmp", "kodi")