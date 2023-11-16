import math
import os
import textwrap
import urllib.request as urllib
from html import escape
# import moviepy.editor as mp

import requests
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageDraw, ImageFont
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    TelegramError,
    Update,
)
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from Exon import dispatcher
# from NekoRobot import tbot as bot
from Exon import telethn as bot
# from NekoRobot.events import register as Cutiepii
from Exon.events import register as Cutiepii
from Exon.modules.disable import DisableAbleCommandHandler

combot_stickers_url = "https://combot.org/telegram/stickers?q="


def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get id sticker",
            parse_mode=ParseMode.HTML,
        )


def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(" ", 1)
    if len(split) == 1:
        msg.reply_text("Provide some name to search for pack.")
        return
    text = requests.get(combot_stickers_url + split[1]).text
    soup = bs(text, "lxml")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text("No results found :(.")
        return
    reply = f"Stickers for *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result["href"]
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.png")
        bot.send_document(chat_id, document=open("sticker.png", "rb"))
        os.remove("sticker.png")
    else:
        update.effective_message.reply_text(
            "Please reply to a sticker for me to upload its PNG."
        )


def kang(update: Update, context: CallbackContext):
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    packnum = 0
    packname = "a" + str(user.id) + "_by_" + context.bot.username
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = (
                    "a"
                    + str(packnum)
                    + "_"
                    + str(user.id)
                    + "_by_"
                    + context.bot.username
                )
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                packname_found = 1
    kangsticker = "kangsticker.png"
    is_animated = False
    is_video = False
    is_gif = False
    file_id = ""

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                is_animated = True
            elif msg.reply_to_message.sticker.is_video :
                is_video = True
            file_id = msg.reply_to_message.sticker.file_id
        # elif msg.reply_to_message.video:
        #     file_id = msg.reply_to_message.video.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif (
            msg.reply_to_message.document
            and not msg.reply_to_message.document.mime_type == "video/mp4"
        ):
            file_id = msg.reply_to_message.document.file_id
        elif msg.reply_to_message.animation:
            file_id = msg.reply_to_message.animation.file_id
            is_gif = True
        else:
            msg.reply_text("Yea, I can't kang that.")

        kang_file = context.bot.get_file(file_id)
        if not is_animated and not (is_video or is_gif):
            kang_file.download("kangsticker.png")
        elif is_animated:
            kang_file.download("kangsticker.tgs")
        elif is_video and not is_gif:
            kang_file.download("kangsticker.webm")
        elif is_gif:
            kang_file.download("kang.mp4")
            # convert_gif("kang.mp4")
            # import moviepy.editor as mp
            # clip = mp.VideoFileClip("kang.gif")
            # clip.write_videofile("kangsticker.webm")

        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🃏"

        if not is_animated and not (is_video or is_gif):
            try:
                im = Image.open(kangsticker)
                maxsize = (512, 512)
                if (im.width and im.height) < 512:
                    size1 = im.width
                    size2 = im.height
                    if im.width > im.height:
                        scale = 512 / size1
                        size1new = 512
                        size2new = size2 * scale
                    else:
                        scale = 512 / size2
                        size1new = size1 * scale
                        size2new = 512
                    size1new = math.floor(size1new)
                    size2new = math.floor(size2new)
                    sizenew = (size1new, size2new)
                    im = im.resize(sizenew)
                else:
                    im.thumbnail(maxsize)
                if not msg.reply_to_message.sticker:
                    im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"Sticker successfully added to [pack](t.me/addstickers/{packname})"
                    + f"\nEmoji is: {sticker_emoji}",
                    parse_mode=ParseMode.MARKDOWN,
                )

            except OSError as e:
                msg.reply_text("I can only kang images m8.")
                print(e)
                return

            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        png_sticker=open("kangsticker.png", "rb"),
                    )
                elif e.message == "Sticker_png_dimensions":
                    im.save(kangsticker, "PNG")
                    context.bot.add_sticker_to_set(
                        user_id=user.id,
                        name=packname,
                        png_sticker=open("kangsticker.png", "rb"),
                        emojis=sticker_emoji,
                    )
                    msg.reply_text(
                        f"Sticker successfully added to [pack](t.me/addstickers/{packname})"
                        + f"\nEmoji is: {sticker_emoji}",
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Stickers_too_much":
                    msg.reply_text("Max packsize reached. Press F to pay respecc.")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    msg.reply_text(
                        "Sticker successfully added to [pack](t.me/addstickers/%s)"
                        % packname
                        + "\n"
                        "Emoji is:" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                print(e)

        elif is_animated:
            packname = "animated" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "animated"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    tgs_sticker=open("kangsticker.tgs", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"Sticker successfully added to [pack](t.me/addstickers/{packname})"
                    + f"\nEmoji is: {sticker_emoji}",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    msg.reply_text(
                        "Sticker successfully added to [pack](t.me/addstickers/%s)"
                        % packname
                        + "\n"
                        "Emoji is:" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                print(e)

        elif is_video or is_gif:
            packname = "video" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 120

            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "animated"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )

                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1

            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    webm_sticker=open("kangsticker.webm", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"Sticker Successfully added to [pack](t.me/addstickers/{packname})"
                    + f"\nEmoji is: {sticker_emoji}",
                    parse_mode=ParseMode.MARKDOWN,
                )

            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        webm_sticker=open("kangsticker.webm", "rb"),
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s)")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    msg.reply_text(
                        f"Sticker Successfully added to [pack](t.me/addsticker/{packname})",
                        +"\n" f"Emoji is: {sticker_emoji}",
                        parse_mode=ParseMode.MARKDOWN,
                    )

    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "🃏"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open("kangsticker.png", "rb"))
            context.bot.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=open("kangsticker.png", "rb"),
                emojis=sticker_emoji,
            )
            msg.reply_text(
                f"Sticker successfully added to [pack](t.me/addstickers/{packname})"
                + f"\nEmoji is: {sticker_emoji}",
                parse_mode=ParseMode.MARKDOWN,
            )
        except OSError as e:
            msg.reply_text("I can only kang images m8.")
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(
                    update,
                    context,
                    msg,
                    user,
                    sticker_emoji,
                    packname,
                    packnum,
                    png_sticker=open("kangsticker.png", "rb"),
                )
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    "Sticker successfully added to [pack](t.me/addstickers/%s)"
                    % packname
                    + "\n"
                    + "Emoji is:"
                    + " "
                    + sticker_emoji,
                    parse_mode=ParseMode.MARKDOWN,
                )
            elif e.message == "Invalid sticker emojis":
                msg.reply_text("Invalid emoji(s).")
            elif e.message == "Stickers_too_much":
                msg.reply_text("Max packsize reached. Press F to pay respect.")
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(
                    "Sticker successfully added to [pack](t.me/addstickers/%s)"
                    % packname
                    + "\n"
                    "Emoji is:" + " " + sticker_emoji,
                    parse_mode=ParseMode.MARKDOWN,
                )
            print(e)
    else:
        packs = "Please reply to a sticker, or image or gif to kang it!\nOh, by the way. here are your packs:\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs += f"[pack](t.me/addstickers/{firstpackname})\n"
                else:
                    packs += f"[pack{i}](t.me/addstickers/{packname})\n"
        else:
            packs += f"[pack](t.me/addstickers/{packname})"
        msg.reply_text(packs, parse_mode=ParseMode.MARKDOWN)
    try:
        if os.path.isfile("kangsticker.png"):
            os.remove("kangsticker.png")
        elif os.path.isfile("kangsticker.tgs"):
            os.remove("kangsticker.tgs")
        elif os.path.isfile("kangsticker.webm"):
            os.remove("kangsticker.webm")
        elif os.path.isfile("kang.mp4"):
            os.remove("kang.mp4")
    except:
        pass


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
    webm_sticker=None,
):
    name = user.first_name
    name = name[:50]
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        if png_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}s kang pack" + extra_version,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}s animated kang pack" + extra_version,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )
        if webm_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}s video kang pack" + extra_version,
                webm_sticker=webm_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(
                "Your pack can be found [here](t.me/addstickers/%s)" % packname,
                parse_mode=ParseMode.MARKDOWN,
            )
        elif e.message in ("Peer_id_invalid", "bot was blocked by the user"):
            msg.reply_text(
                "Contact me in PM first.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Start",
                                url=f"t.me/{context.bot.username}",
                            ),
                        ],
                    ],
                ),
            )
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            msg.reply_text(
                "Sticker pack successfully created. Get it [here](t.me/addstickers/%s)"
                % packname,
                parse_mode=ParseMode.MARKDOWN,
            )
        return

    if success:
        msg.reply_text(
            "Sticker pack successfully created. Get it [here](t.me/addstickers/%s)"
            % packname,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")


# if your are reading this, it took me 2 hours to make delsticker
def delsticker(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
    else:
        update.effective_message.reply_text(
            "Please reply to the sticker which you want to delete from your pack"
        )
    try:
        context.bot.delete_sticker_from_set(file_id)
        msg.reply_text(
            "Deleted That Sticker from your Pack!\nRemove and Re-Add the Pack to see the changes."
        )

    except TelegramError as e:
        print(e)
        if e.message == "Stickerset_invalid":
            msg.reply_text(
                "Maybe the sticker pack is not yours or the pack was not made by me!",
                parse_mode=ParseMode.MARKDOWN,
            )


Credit = "This Plugin Made by Kakashi (@YeahOffline), if you're using this code in your bot. there is no issue but don't remove this line"


@asux(pattern="^/mmf ?(.*)")
async def memify(message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.err("LMAO no one's gonna help you, if u use .help now then u **Gey**")
        await message.client.send_sticker(
            sticker="CAADAQADhAAD3gkwRviGxMVn5813FgQ", chat_id=message.chat.id)
        return
    if not (replied.photo or replied.sticker or replied.animation):
        await message.err("Bruh, U Comedy me? Read help or gtfo (¬_¬)")
        return
    if not os.path.isdir(config.Dynamic.DOWN_PATH):
        os.makedirs(config.Dynamic.DOWN_PATH)
    await message.edit("He he, let me use my skills")
    dls = await message.client.download_media(
        message=message.reply_to_message,
        file_name=config.Dynamic.DOWN_PATH,
        progress=progress,
        progress_args=(message, "Trying to Posses given content")
    )
    dls_loc = os.path.join(config.Dynamic.DOWN_PATH, os.path.basename(dls))
    if replied.sticker and replied.sticker.file_name.endswith(".tgs"):
        await message.edit("OMG, an Animated sticker ⊙_⊙, lemme do my bleck megik...")
        png_file = os.path.join(config.Dynamic.DOWN_PATH, "meme.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dls_loc} {png_file}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(dls_loc)
        if not os.path.lexists(png_file):
            await message.err("This sticker is Gey, i won't memify it ≧ω≦")
            raise Exception(stdout + stderr)
        dls_loc = png_file
    elif replied.animation:
        await message.edit("Look it's GF. Oh, no it's just a Gif ")
        jpg_file = os.path.join(config.Dynamic.DOWN_PATH, "meme.jpg")
        await take_screen_shot(dls_loc, 0, jpg_file)
        os.remove(dls_loc)
        if not os.path.lexists(jpg_file):
            await message.err("This Gif is Gey (｡ì _ í｡), won't memify it.")
            return
        dls_loc = jpg_file
    await message.edit("Decoration Time ≧∇≦, I'm an Artist")
    webp_file = await draw_meme_text(dls_loc, message.input_str)
    await message.client.send_sticker(chat_id=message.chat.id,
                                      sticker=webp_file,
                                      reply_to_message_id=replied.id)
    await message.delete()
    os.remove(webp_file)


async def draw_meme_text(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    m_font = ImageFont.truetype(
        "userge/plugins/fun/memify/resources/MutantAcademyStyle.ttf",
        int((70 / 640) * i_width)
    )
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ''
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(xy=(((i_width - u_width) / 2) - 1, int((current_h / 640)*i_width)),
                      text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=(((i_width - u_width) / 2) + 1, int((current_h / 640)*i_width)),
                      text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=((i_width - u_width) / 2, int(((current_h / 640)*i_width)) - 1),
                      text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=(((i_width - u_width) / 2), int(((current_h / 640)*i_width)) + 1),
                      text=u_text, font=m_font, fill=(0, 0, 0))

            draw.text(xy=((i_width - u_width) / 2, int((current_h / 640)*i_width)),
                      text=u_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(((i_width - u_width) / 2) - 1, i_height - u_height - int((20 / 640)*i_width)),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, i_height - u_height - int((20 / 640)*i_width)),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640)*i_width)) - 1),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640)*i_width)) + 1),
                text=l_text, font=m_font, fill=(0, 0, 0))

            draw.text(
                xy=((i_width - u_width) / 2, i_height - u_height - int((20 / 640)*i_width)),
                text=l_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(config.Dynamic.DOWN_PATH, image_name)
    img.save(webp_file, "WebP")
    return webp_file

__help__ = """
  • `/stickerid` : reply to a sticker to me to tell you its file ID.
  • `/getsticker` : reply to a sticker to me to upload its raw PNG file.
  • `/kang` : reply to a sticker to add it to your pack.
  • `/delkang` : reply to a Sticker to remove it from your pack
  • `/mmf` : memefiy any sticker and image.
  • `/stickers` : Find stickers for given term on combot sticker catalogue
"""

__mod_name__ = "Stickers"
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid, run_async=True)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker, run_async=True)
KANG_HANDLER = DisableAbleCommandHandler(["kang", "steal"], kang, run_async=True)
DELKANG_HANDLER = DisableAbleCommandHandler(
    ["delsticker", "delkang"], delsticker, run_async=True
)
STICKERS_HANDLER = DisableAbleCommandHandler("stickers", cb_sticker, run_async=True)

dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
dispatcher.add_handler(DELKANG_HANDLER)
