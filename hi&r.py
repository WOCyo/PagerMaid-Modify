""" Message related utilities. """

import requests
import json
from telethon.tl.functions.messages import DeleteChatUserRequest
from telethon.tl.functions.channels import LeaveChannelRequest, GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import ChatIdInvalidError
from distutils2.util import strtobool
from pagermaid import bot, log, config
from pagermaid.listener import listener


@listener(outgoing=True, command="r",
          description="在当前会话复读回复的消息。（需要回复一条消息）",
          parameters="<次数>")
async def re(context):
    """ Forwards a message into this group """
    reply = await context.get_reply_message()
    if reply:
        if context.arguments == '':
            num = 1
        else:
            try:
                num = int(context.arguments)
                if num > 100:
                    await context.edit('呜呜呜出错了...这个数字太大惹')
                    return True
            except:
                await context.edit('呜呜呜出错了...可能参数不是数字')
                return True
        await context.delete()
        for nums in range(0, num):
            await reply.forward_to(int(context.chat_id))
    else:
        await context.edit("出错了呜呜呜 ~ 您好像没有回复一条消息。")


@listener(outgoing=True, command="hi",
          description="发送一句一言")
async def hitokoto(context):
    """ Get hitokoto.cn """
    hitokoto_json = json.loads(requests.get("https://v1.hitokoto.cn/?charset=utf-8").content.decode("utf-8"))
    if hitokoto_json['type'] == 'a':
        hitokoto_type = '动画'
    elif hitokoto_json['type'] == 'b':
        hitokoto_type = '漫画'
    elif hitokoto_json['type'] == 'c':
        hitokoto_type = '游戏'
    elif hitokoto_json['type'] == 'd':
        hitokoto_type = '文学'
    elif hitokoto_json['type'] == 'e':
        hitokoto_type = '原创'
    elif hitokoto_json['type'] == 'f':
        hitokoto_type = '来自网络'
    elif hitokoto_json['type'] == 'g':
        hitokoto_type = '其他'
    elif hitokoto_json['type'] == 'h':
        hitokoto_type = '影视'
    elif hitokoto_json['type'] == 'i':
        hitokoto_type = '诗词'
    elif hitokoto_json['type'] == 'j':
        hitokoto_type = '网易云'
    elif hitokoto_json['type'] == 'k':
        hitokoto_type = '哲学'
    elif hitokoto_json['type'] == 'l':
        hitokoto_type = '抖机灵'
    await context.edit(f"{hitokoto_json['hitokoto']} - {hitokoto_json['from']}（{str(hitokoto_type)}）")


