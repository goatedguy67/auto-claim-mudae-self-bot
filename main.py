from datetime import timedelta, timezone
from typing import Any
from tomllib import load

from src.MudaeBot import MudaeBot

settings: dict[str, Any] = load(open("settings.toml", "rb"))
settings = load(open("./bot-settings.toml", "rb"))

channels_information = {}
utc_delta: int = settings["UTC_delta"]


for information in settings["channels_information"]:
    channels_information[information["id"]] = {
        "settings": information["settings"],
    }


MUDAE_ID = 432610292342587392
TIME_ZONE = timezone(timedelta(hours=utc_delta))

bot = MudaeBot()
bot.run(settings["token"], reconnect=True)
