import subprocess
import sys
import os

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")

subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)
subprocess.run(["npm", "run", "dev"], cwd=frontend_dir, check=True, shell=True)
