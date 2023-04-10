

from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.raw.functions import Ping
from pixsuvy import LOG_GROUP, OWNER_ID, SUDO_USERS, Mbot,AUTH_CHATS
from os import execvp,sys

@Mbot.on_message(filters.command("start"))
async def start(client,message):
    reply_markup = [[
        InlineKeyboardButton(
            text="Developer", url="https://t.me/shotta_flow_xd"),
        InlineKeyboardButton(
            text="Repo",
            url="https://github.com/slrub/gts-music-downloader"),
        InlineKeyboardButton(text="Help",callback_data="helphome")
        ]]
    if message.chat.type != "private" and message.chat.id not in AUTH_CHATS and message.from_user.id not in SUDO_USERS:
        return await message.reply_text("This Bot Will Not Work In Groups Unless It's Authorized.",
                    reply_markup=InlineKeyboardMarkup(reply_markup))
    return await message.reply_text(f"Hello {message.from_user.first_name}, I'm a PIXSUVY TG MUSIC DOWNLOADER Bot. I Currently Support Download from Youtube.",
                    reply_markup=InlineKeyboardMarkup(reply_markup))

@Mbot.on_message(filters.command("restart") & filters.chat(OWNER_ID) & filters.private)
async def restart(_,message):
    await message.delete()
    execvp(sys.executable,[sys.executable,"-m","pixsuvy"])

@Mbot.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_,message):
    await message.reply_document("bot.log")

@Mbot.on_message(filters.command("ping"))
async def ping(client,message):
    start = datetime.now()
    await client.send(Ping(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    await message.reply_text(f"**Pong!**\nResponse time: `{ms} ms`")

HELP = {
    "Youtube": "Send **Youtube** Link in Chat to Download Song.",
    "Spotify": "Send **Spotify** Track/Playlist/Album/Show/Episode's Link. I'll Download It For You.",
    "Deezer": "Send Deezer Playlist/Album/Track Link. I'll Download It For You.",
}


@Mbot.on_message(filters.command("help"))
async def help(_,message):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]

    await message.reply_text(f"Hello **{message.from_user.first_name}**, I'm **GTS-MUSIC-DOWNLOADER**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))

@Mbot.on_callback_query(filters.regex(r"help_(.*?)"))
async def helpbtn(_,query):
    i = query.data.replace("help_","")
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Back",callback_data="helphome")]])
    text = f"Help for **{i}**\n\n{HELP[i]}"
    await query.message.edit(text = text,reply_markup=button)

@Mbot.on_callback_query(filters.regex(r"helphome"))
async def help_home(_,query):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    await query.message.edit(f"Hello **{query.from_user.first_name}**, I'm **GTS-MUSIC-DOWNLOADER**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))
