from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from pyrogram import Client, filters
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from logger import logging
import time
import asyncio
from pyrogram.types import User, Message
from details import api_id, api_hash, bot_token, log_channel
import sys
import re
import os

botStartTime = time.time()
bot = Client("bot",
             bot_token= "__", 
             api_id= _,
             api_hash= "__")

#global Variables 
log_channel_id = -__

@bot.on_message(filters.command(["Start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"Hello I Am Active You Can Use Me")


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("🛑🛑**STOPPED**🛑🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


#-------------TXT Uploader Commands ---------------

@bot.on_message(filters.command(["GURJAR"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"**Hey Send txt file**")
    input: Message = await bot.listen(editable.chat.id)
    if input.document:
        x = await input.download()
        await bot.send_document(log_channel_id, x)
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"GURJAR"

        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                links.append(i.split("://", 1))
            os.remove(x)
        except:
            await m.reply_text("Invalid file input.🥲")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send df for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'df':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution:**\n\n144\n240\n360\n480\n720\n1080\n\n **Please Choose Quality**\n\n")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "df":
            res = "1280x720"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        elif raw_text2 == "144":
            res = "256x144" 
        else: 
            res = "UN"
    except Exception:
        res = "UN"
    
    await editable.edit("**Enter Your Name or send `df` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == 'df':
        CR = "GURJAR"
    else:
        CR = raw_text3

    await editable.edit("Now send the **To set the thumbnail upload an image or send `no`\n or send `df` for default use")
    input6 = await bot.listen(editable.chat.id)

    if input6.photo:
        thumb = await input6.download()
    else:
        raw_text6 = input6.text
        if raw_text6 == "df":
            thumb = "luminant.jpg"
        elif raw_text6.startswith("http://") or raw_text6.startswith("https://"):
            getstatusoutput(f"wget '{raw_text6}' -O 'raw_text6.jpg'")
            thumb = "raw_text6.jpg"
        else:
            thumb = "no"
    await input6.delete(True)
    await editable.delete()
    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            if len(links[i]) != 2 or not links[i][1]:
                # If the link is empty or not properly formatted, continue to the next iteration
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
                await m.reply_text(f"No link found for **{name}**.")
                continue
            try:
                V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
                url = "https://" + V

                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                            text = await resp.text()
                            url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

                elif 'videos.classplusapp' or "cpvod.testbook.com" in url:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

                elif '/master.mpd' in url:
                    id =  url.split("/")[-2]
                    url =  "https://d1d34p8vz63oiq.cloudfront.net" + id + "/master.m3u8"

                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'

                if "youtu" in url:
                    ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                else:
                    ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

                if "jw-prod" in url:
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                else:
                    cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

                cc = f'**[📹]Video_ID : {str(count).zfill(3)}.**\n\n**Video Name :** {name1} ({res}) [FRIEND].mkv\n\n**Batch Name :** {b_name}\n\n**Downloaded By : {CR}**'
                cc1 = f'**[📁]File_ID : {str(count).zfill(3)}.**\n\n**File Name :** {name1} [FRIEND].pdf\n\n**Batch Name :** {b_name}\n\n**Downloaded By : {CR}**'
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        message = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)  # Sending copy to log channel
                        file_id = message.document.file_id
                        await bot.send_document(chat_id=log_channel_id, document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        message = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        file_id = message.document.file_id
                        await bot.send_document(chat_id=log_channel_id, document=file_id, caption=cc1) 
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    prog = await m.reply_text(f"**Downloading📥:-**\n\n** Video Name :-** `{name}\n\n**Bot Made By FRIEND** ")
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, log_channel_id)
                    count += 1
            except Exception as e:
                logging.error(e)
                await bot.send_message(log_channel_id, f"❌ **Failed To Download** ❌\n**Name**: {name}\n**Link**: `{url}`\n\n **Bot Made By FRIEND** ", disable_notification=True)
                await m.reply_text(f"**Failed To Download ❌**\n**Name** - {name}\n**Link** - `{url}`**Bot Made By FRIEND** ")
                time.sleep(3)
                continue
    except Exception as e:
        await m.reply_text(e)
    await bot.send_message(log_channel_id, "Done🚦")
    await m.reply_text("Done🚦")

bot.run()
