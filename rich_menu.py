"""
Modify from https://github.com/line/line-bot-sdk-python/blob/master/examples/rich-menu/app.py
"""

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
    MessageAction
)
from linebot.models.actions import RichMenuSwitchAction
from linebot.models.rich_menu import RichMenuAlias

line_bot_api = LineBotApi("78jU0vU39l5DQg1lgllyOssB3nh+e1SZzZ7wrGZk4BF80JARZWq9j9OmaCKgPwFDr0hePiFM4QW1aSiDlE0fOKSRASfLmC3B6ut9E/Hn+IWNLeZsO7TQJVu47NoGC3JxyI0eL5vDjfuiW2q25sZxogdB04t89/1O/w1cDnyilFU=")

def rich_menu_object_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "Quick Guide",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {"x": 113, "y": 45, "width": 1036, "height": 762},
                "action": {"type": "message", "text": "introduction"}
            },
            {
                "bounds": {"x": 1321, "y": 45, "width": 1036, "height": 762},
                "action": {"type": "message", "text": "lab"}
            },
            {
                "bounds": {"x": 113, "y": 910, "width": 1036, "height": 762},
                "action": {"type": "message", "text": "github"}
            },
            {
                "bounds": {"x": 1321, "y": 910, "width": 1036, "height": 762},
                "action": {"type": "message", "text": "project"}
            }
        ]
    }


def create_action(action):
    if action['type'] == 'message':
        return MessageAction(type=action['type'], text=action.get('text'))
    else:
        return RichMenuSwitchAction(
            type=action['type'],
            rich_menu_alias_id=action.get('richMenuAliasId'),
            data=action.get('data')
        )


def main():
    rich_menu_object = rich_menu_object_json()
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object['areas']
    ]

    rich_menu_to_a_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object['size']['width'], height=rich_menu_object['size']['height']),
        selected=rich_menu_object['selected'],
        name=rich_menu_object['name'],
        chat_bar_text=rich_menu_object['name'],
        areas=areas
    )

    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_a_create)

    with open('./public/all.jpg', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

    line_bot_api.set_default_rich_menu(rich_menu_id)

    alias = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias',
        rich_menu_id=rich_menu_id
    )
    line_bot_api.create_rich_menu_alias(alias)

    print('success')

main()