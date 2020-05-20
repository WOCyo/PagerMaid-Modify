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


@listener(outgoing=True, command="userid",
          description="查询您回复消息的发送者的用户ID。")
async def userid(context):
    """ Query the UserID of the sender of the message you replied to. """
    message = await context.get_reply_message()
    if message:
        user_id = message.sender.id
        if message.sender.username:
            target = "@" + message.sender.username
        else:
            try:
                target = "**" + message.sender.first_name + "**"
            except TypeError:
                target = "**" + "死号" + "**"
        if not message.forward:
            await context.edit(
                f"**以下是被回复消息的信息** \n\n**道纹:** {target} \n"
                f"**用户ID:** `{user_id}`"
             )
        else:
            try:
                user_f_id = message.forward.sender.id
                if message.forward.sender.username:
                    target_f = "@" + message.forward.sender.username
                else:
                    target_f = "*" + message.forward.sender.first_name + "*"
                await context.edit(
                    f"**以下是被回复消息的信息** \n\n**道纹:** {target} \n"
                    f"**用户ID:** `{user_id}` \n\n**以下是转发来源信息** \n\n"
                    f"**道纹:** {target_f} \n"
                    f"**用户ID:** `{user_f_id}`"
                 )
            except:
                await context.edit(
                    f"**以下是被回复消息的信息** \n\n**道纹:** {target} \n"
                    f"**用户ID:** `{user_id}` \n\n**此消息没有包含被转发用户的信息** \n\n"
                 )
    else:
        await context.edit("出错了呜呜呜 ~ 无法获取所回复消息的信息。")


@listener(outgoing=True, command="chatid",
          description="查询当前会话的 chatid 。")
async def chatid(context):
    """ Queries the chatid of the chat you are in. """
    await context.edit("ChatID: `" + str(context.chat_id) + "`")


@listener(outgoing=True, command="uslog",
          description="转发一条消息到日志。",
          parameters="<string>")
async def uslog(context):
    """ Forwards a message into log group """
    if strtobool(config['log']):
        if context.reply_to_msg_id:
            reply_msg = await context.get_reply_message()
            await reply_msg.forward_to(int(config['log_chatid']))
        elif context.arguments:
            await log(context.arguments)
        else:
            await context.edit("出错了呜呜呜 ~ 无效的参数。")
            return
        await context.edit("已记录。")
    else:
        await context.edit("出错了呜呜呜 ~ 日志记录已禁用。")


@listener(outgoing=True, command="log",
          description="静默转发一条消息到日志。",
          parameters="<string>")
async def log(context):
    """ Forwards a message into log group """
    if strtobool(config['log']):
        if context.reply_to_msg_id:
            reply_msg = await context.get_reply_message()
            await reply_msg.forward_to(int(config['log_chatid']))
        elif context.arguments:
            await log(context.arguments)
        else:
            await context.edit("出错了呜呜呜 ~ 无效的参数。")
            return
        await context.delete()
    else:
        await context.edit("出错了呜呜呜 ~ 日志记录已禁用。")


@listener(outgoing=True, command="re",
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


@listener(outgoing=True, command="leave",
          description="说 再见 然后离开会话。")
async def leave(context):
    """ It leaves you from the group. """
    if context.is_group:
        await context.edit("贵群真是浪费我的时间，再见。")
        try:
            await bot(DeleteChatUserRequest(chat_id=context.chat_id,
                                            user_id=context.sender_id
                                            ))
        except ChatIdInvalidError:
            await bot(LeaveChannelRequest(context.chat_id))
    else:
        await context.edit("出错了呜呜呜 ~ 当前聊天似乎不是群聊。")


@listener(outgoing=True, command="meter2feet",
          description="将米转换为英尺。",
          parameters="<meters>")
async def meter2feet(context):
    """ Convert meter to feet. """
    if not len(context.parameter) == 1:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    meter = float(context.parameter[0])
    feet = meter / .3048
    await context.edit(f"将 {str(meter)} 米装换为了 {str(feet)} 英尺。")


@listener(outgoing=True, command="feet2meter",
          description="将英尺转换为米。",
          parameters="<feet>")
async def feet2meter(context):
    """ Convert feet to meter. """
    if not len(context.parameter) == 1:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    feet = float(context.parameter[0])
    meter = feet * .3048
    await context.edit(f"将 {str(feet)} 英尺转换为了 {str(meter)} 米。")


@listener(outgoing=True, command="hitokoto",
          description="发送一句一言")
async def hitokoto(context):
    """ Get hitokoto.cn """
    hitokoto_while = 1
    try:
        hitokoto_json = json.loads(requests.get("https://v1.hitokoto.cn/?charset=utf-8").content.decode("utf-8"))
    except (ValueError):
        while hitokoto_while < 10:
            hitokoto_while += 1
            try:
                hitokoto_json = json.loads(requests.get("https://v1.hitokoto.cn/?charset=utf-8").content.decode("utf-8"))
                break
            except:
                continue
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


@listener(outgoing=True, command="source",
          description="显示原始 PagerMaid git 存储库的URL。")
async def source(context):
    """ Outputs the git repository URL. """
    await context.edit("https://git.stykers.moe/scm/~stykers/pagermaid.git")


@listener(outgoing=True, command="site",
          description="显示原始 PagerMaid 项目主页的URL。")
async def site(context):
    """ Outputs the site URL. """
    await context.edit("https://katonkeyboard.moe/pagermaid.html")
