import os
from folder import folder


with open(os.path.join(folder, './Edition_logs.txt'), 'r', encoding='UTF-8') as f:
    Edition_logs: str = f.read()
