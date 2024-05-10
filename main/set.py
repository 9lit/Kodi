import os, sys
# import re
import subprocess
# from main.tools import write_file, read_file
# from main.config import Config

# class SetConfig():

#     def __init__(self, command:str) -> None:

#         print(command)
#         command = command.replace("--", "").split("=")
#         self.set_mode = None
#         self.config_yaml_path = None
#         self.py_config_path = os.path.join(Config.HOME, "main", "config.py")
#         self.py_config_text = read_file.txt(path=self.py_config_path)
#         self.pattern = r"config_path = .*"
#         if len(command) == 2:
#             self.set_mode, self.config_yaml_path = command
#         else:
#             self.set_mode = command[0]
    

#     # 替换文本内容
#     def sub(self):
#         if "\\" in self.config_yaml_path:
#             self.config_yaml_path = self.config_yaml_path.replace("\\", "/")
#         self.new_py_config_text  = "config_path = '%s'" % self.config_yaml_path
#         new_config = re.sub(self.pattern, self.new_py_config_text, self.py_config_text, count=1)
#         write_file.txt(self.py_config_path, content=new_config)

#     # 移动文件
#     def move(self):

#         subprocess.run("cp '%s' '%s'" % (self.source, self.target))

#     def run(self):

#         if self.set_mode == "set":
#             if self.config_yaml_path:
#                 # print(self.config_yaml_path)
#                 self.sub()
#                 print(f"新的配置文件路径为{self.config_yaml_path}")
#                 print(f"请将配置文件移动此文件夹")
#             else:
#                 print("请检查替换路径")

#         if self.set_mode == "reset" or "init":
#             if self.set_mode == "reset":
#                 self.config_yaml_path =  os.path.join(Config.HOME, "config_perform.yml")
#                 self.sub()
#                 print("配置文件重置成功")
            
#             self.source = os.path.join(Config.HOME, "config.yml")
#             self.target = os.path.join(Config.HOME, "config_perform.yml")
#             self.move()

#             if self.set_mode == "init":
#                 print("配置文件初始化成功")

class Config():

    def run():

        if len(sys.argv) > 1 and sys.argv[2] == "init": 

            home_dir = os.path.dirname(__file__)
            home_dir, basename = home_dir.split(home_dir)

            source = os.path.join(home_dir, 'modular', "config.yml")
            target = os.path.join(home_dir, "config_perform.yml")

            subprocess.run("cp '%s' '%s'" % (source, target))

        else:
            print("请输入命令 python set.py config init")
                