import re

from pyrogram import filters

from pyrogram.types import Message

from Exon import Abishnoi

@Abishnoi.on_message(

    filters.text

    & filters.regex(r"\b[Ii][\'’]?[Aa][Mm]\b")

    & ~filters.via_bot

    & ~filters.bot,

)

async def upvote(_, message: Message):

    text = message.text

    match = re.search(r"(?<=\bI[\'’]?[Aa][Mm]\b\s)\w+", text)

    if match:

        word = match.group()

        word = word.lower().capitalize()

        return await message.reply_text(f"Hello {word}! I am Dad.")

    return
