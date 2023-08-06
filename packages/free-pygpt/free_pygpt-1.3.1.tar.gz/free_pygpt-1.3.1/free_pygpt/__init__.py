#Using template from https://github.com/Minori101/Amino.fix/blob/main/aminofix/__init__.py :D THANKS

__title__ = 'free-pygpt'
__author__ = 'nxSlayer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 nxSlayer'


from requests import get
from json import loads

__newest__ = loads(get("https://pypi.org/pypi/free-pygpt/json").text)["info"]["version"]

if '1.3.1' != __newest__:
    print(f"(free-gpt) There is a new version, please update for better results")