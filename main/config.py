import os
from main.tools import read_file

# user_home = os.getenv("HOME")
now_path = os.path.dirname(__file__)
home_dir, filename = os.path.split(now_path)

config_path = os.path.join(home_dir, "config_perform.yml")

class Config:

    config = read_file.yaml(config_path)
    if not config:
        print(f"没有获取到配置文件,请重新设置, 请运行默认命令 python run.py config init")
        exit()
    
    HOME = home_dir
    PLAYER_NAME = config['default_template']
    SCRAPER_NAME = config['default_scraper']

    # 播放器的配置文件     
    template_player = config['template'][PLAYER_NAME]
    TEMPLATE_EPISODE =  os.path.join(home_dir, template_player['episode']) 

    # 刮削器的配置
    scraper_config = config[SCRAPER_NAME]
    scraper_url = scraper_config['url']
    # 获取刮削器的令牌
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
    PATH = config['path']
    
    # 是否刮削全部
    SCRAPER_ALL = config['scraper_all']

    # 是否刮削图片
    DOWNLOAD_IMAGE = config["download_image"]

    TMDB_CACHE = os.path.join(HOME, "tmp", "tmdb")
