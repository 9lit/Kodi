import os
from main.tools import read_file

# user_home = os.getenv("HOME")
now_path = os.path.dirname(__file__)
home_dir, filename = os.path.split(now_path)

config_path = os.path.join(home_dir, "config_perform.yml")

class Config:

    _config = read_file.yaml(config_path)
    if not _config:
        print(f"没有获取到配置文件,请重新设置, 请运行默认命令 python run.py config init")
        exit()
    
    HOME = home_dir
    PLAYER_NAME = _config['default_template']
    SCRAPER_NAME = _config['default_scraper']

    # 播放器的配置文件     
    _template_player = _config['template'][PLAYER_NAME]
    ## 将模板路径转换为当前系统的路径
    _template_player_episode = _template_player['episode'].replace("\\", "/").split("/")
    _template_player_episode = os.path.join(*_template_player_episode)
    TEMPLATE_EPISODE =  os.path.join(home_dir, _template_player_episode)

    # 刮削器的配置
    _scraper_config = _config[SCRAPER_NAME]
    scraper_url = _scraper_config['url']
    # 获取刮削器的令牌
    _auth = os.getenv(_scraper_config['evn_auth'])
    _confi_auth = _scraper_config['authorization']
    if _auth or _confi_auth:
        AUTHORIZATION = _auth if _auth else _confi_auth
    else:
        print("获取 令牌失败,请检查令牌")
        exit()

    LANGUAGE = _scraper_config['language']
    THUMB_IMAGE_URL = scraper_url['thumb_image_url']
    THUMB_PERSON_URL = scraper_url['thumb_person_url']

    # 刮削路径
    PATH = _config['path']
    
    # 是否刮削全部
    SCRAPER_ALL = _config['scraper_all']

    # 是否刮削图片
    DOWNLOAD_IMAGE = _config["download_image"]

    TMDB_CACHE = os.path.join(HOME, "tmdb")

    _info = f"""
项目目录: {HOME},
配置文件位置: {config_path},
刮削路径: {PATH},
是否刮削全部: {SCRAPER_ALL},
是否刮削图片: {DOWNLOAD_IMAGE},
"""
    print(_info)