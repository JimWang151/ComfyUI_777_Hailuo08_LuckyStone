# Made by Jim.Wang V1 for ComfyUI
import os
import subprocess
import importlib.util
import sys
import filecmp
import shutil

import __main__

python = sys.executable




from .HailuoLuckyStone import LuckyStone

NODE_CLASS_MAPPINGS = {
    "LuckyStone":LuckyStone
}


print('\033[34mHailuoLuckyStone LuckyStone Nodes: \033[92mLoaded\033[0m')