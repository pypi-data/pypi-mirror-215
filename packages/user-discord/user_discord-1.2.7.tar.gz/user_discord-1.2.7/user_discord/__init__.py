#Using template from https://github.com/Minori101/Amino.fix/blob/main/aminofix/__init__.py :D THANKS

__title__ = 'user_discord'
__author__ = 'nxSlayer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 nxSlayer'

from .user_discord import SocketDiscord
from .user_discord import ClientDiscord
from .lib.utils import objects
from .lib.utils import payloads

from requests import get
from json import loads

__newest__ = loads(get("https://pypi.org/pypi/user-discord/json").text)["info"]["version"]

if '1.2.7' != __newest__:
    print(f"(user-discord) There is a new version, please update for better results")