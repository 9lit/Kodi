import sys
from main import set

# import json

class Usage:
    """基于 tmdb 和 kodi 的视频自动刮削脚本.

用法: 
python run.py 执行自动刮削脚本
python run.py config [参数] 编辑配置文件

参数:
config:
  set 设置配置文件位置, 修改 config.py 中的 config_perform.yml 位置
  init 初始化配置文件, 复制 config.yml 文件 并重新命名为 config_perform.yml
  reset 重置配置文件, 复制 config.yaml 文件,并重命名, 且修改配置 config.py 中 config_perform.yml 位置
"""
    pass

class ScrapeInfo():

    def __init__(self) -> None:
        self.matedata = None
        self.info = None
        self.argv = sys.argv
        self.len_argv = len(self.argv)

    def scraper(self):
        import modular.scraper.main
        self.matedata = modular.scraper.main.run(self.info)
        if self.matedata:
            pass
        else:
            print("没有搜索数据, 请检查文件或者刮削api")
            exit()

    def player(self):
        import modular.player.main
        modular.player.main.run(self.matedata)


    def file(self):
        from main.file import File
        self.info = File().run()
        if self.info['episode']:
            print(self.info)
        else:
            print("没有需要刮削的文件")
            exit()

    def config(self):
        
        if self.len_argv > 1 and self.argv[1] == "config":
            if self.len_argv == 3:
                if not set.Config.run():
                    print(Usage.__doc__)
                else:
                    print("配置文件设置成功")
            else:
                print(Usage.__doc__)
        
            exit()
        else:
            pass


    def run(self):
        self.config()
        self.file()
        self.scraper()           
        self.player()

if __name__ == "__main__":
    s = ScrapeInfo().run()
            
                
        
                    



