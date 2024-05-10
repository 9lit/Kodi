import os, sys
import subprocess

class Config:

    def run():

        if sys.argv[2] == "init": 
            home_dir = os.path.dirname(__file__)
            home_dir, basename = os.path.split(home_dir)

            source = os.path.join(home_dir, 'modular', "config.yml")
            target = os.path.join(home_dir, "config_perform.yml")

            subprocess.run("cp '%s' '%s'" % (source, target))

        else:
            return False