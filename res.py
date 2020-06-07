""" Pagermaid res plugin. """

from telethon.events import StopPropagation
from pagermaid import persistent_vars, log
from pagermaid.listener import listener

persistent_vars.update({'res': {'enabled': False, 'message': None, 'amount': 0}})


@listener(outgoing=True, command="res",
          description="自动回复。当参数为 false 时，表示禁用自动回复",
          parameters="<message>")
async def res(context):
    """ Enables the auto responder. """
    message = "我还在睡觉... ZzZzZzZzZZz"
    if context.arguments:
        message = context.arguments
        if message == "false":
            if persistent_vars['res']['enabled']:
                await context.edit("成功禁用自动响应器。")
                await log(f"禁用自动响应器。 在闲置期间 {persistent_vars['res']['amount']}"
                          f" 条消息被自动回复")
                persistent_vars.update({'res': {'enabled': False, 'message': None, 'amount': 0}})
            else:
                await context.edit("未启用自动响应器。")
            return
        else:
            pass
    await context.edit("成功启用自动响应器。")
    await log(f"启用自动响应器，将自动回复 `{message}`.")
    persistent_vars.update({'res': {'enabled': True, 'message': message, 'amount': 0}})
    raise StopPropagation


@listener(incoming=True, ignore_edited=True)
async def reply_res(context):
    if persistent_vars['res']['enabled']:
        if context.is_private or context.message.mentioned:
            persistent_vars['res']['amount'] += 1
            await context.reply(persistent_vars['res']['message'])