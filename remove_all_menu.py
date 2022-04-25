import os
import sys

from linebot import (
    LineBotApi,
)

from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction
)
from linebot.models.actions import RichMenuSwitchAction
from linebot.models.rich_menu import RichMenuAlias

line_bot_api = LineBotApi("78jU0vU39l5DQg1lgllyOssB3nh+e1SZzZ7wrGZk4BF80JARZWq9j9OmaCKgPwFDr0hePiFM4QW1aSiDlE0fOKSRASfLmC3B6ut9E/Hn+IWNLeZsO7TQJVu47NoGC3JxyI0eL5vDjfuiW2q25sZxogdB04t89/1O/w1cDnyilFU=")


rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    # print(rich_menu.rich_menu_id)
    line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)