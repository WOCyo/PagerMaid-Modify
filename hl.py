""" PagerMaid module for adding captions to image. """

from os import remove
from magic import Magic
from pygments import highlight as syntax_highlight
from pygments.formatters import img
from pygments.lexers import guess_lexer
from pagermaid import log, module_dir
from pagermaid.listener import listener
from pagermaid.utils import execute, upload_attachment


@listener(outgoing=True, command="hl",
          description="生成有语法高亮显示的图片。",
          parameters="<string>")
async def highlight(context):
    """ Generates syntax highlighted images. """
    if context.fwd_from:
        return
    reply = await context.get_reply_message()
    reply_id = None
    await context.edit("正在渲染图片，请稍候 . . .")
    if reply:
        reply_id = reply.id
        target_file_path = await context.client.download_media(
            await context.get_reply_message()
        )
        if target_file_path is None:
            message = reply.text
        else:
            if Magic(mime=True).from_file(target_file_path) != 'text/plain':
                message = reply.text
            else:
                with open(target_file_path, 'r') as file:
                    message = file.read()
            remove(target_file_path)
    else:
        if context.arguments:
            message = context.arguments
        else:
            await context.edit("`出错了呜呜呜 ~ 无法检索目标消息。`")
            return
    lexer = guess_lexer(message)
    formatter = img.JpgImageFormatter(style="colorful")
    result = syntax_highlight(message, lexer, formatter, outfile=None)
    await context.edit("正在上传图片中 . . .")
    await context.client.send_file(
        context.chat_id,
        result,
        reply_to=reply_id
    )
    await context.delete()


async def handle_failure(context, target_file_path):
    await context.edit("出错了呜呜呜 ~ 请向原作者报告此问题。")
    try:
        remove("result.png")
        remove(target_file_path)
    except FileNotFoundError:
        pass
