import logging
import subprocess
import datetime
import asyncio
import os
import requests
import time
from p_bar import progress_bar
import aiohttp
import tgcrypto
import aiofiles
from pyrogram.types import Message
from pyrogram import Client, filters
import re

def duration(filename):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", filename
    ],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


async def aio(url, name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k


async def vision(url, name, cookies):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, cookies = cookies) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka     


def get_link(url):
   urlx = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',url)
   return urlx[0]


async def download(url, name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka


def parse_vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = []
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ", 2)
            try:
                if "RESOLUTION" not in i[2] and i[
                        2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info


def vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ", 3)
            try:
                if "RESOLUTION" not in i[2] and i[
                        2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])

                    # temp.update(f'{i[2]}')
                    # new_info.append((i[2], i[0]))
                    #  mp4,mkv etc ==== f"({i[1]})"

                    new_info.update({f'{i[2]}': f'{i[0]}'})

            except:
                pass
    return new_info


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'


def old_download(url, file_name, chunk_size=1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"


async def download_video(url, cmd, name):
    download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
    logging.info(download_cmd)
    k = os.system(download_cmd)
    try:
        if os.path.isfile(name):
            return name
        elif os.path.isfile(f"{name}.webm"):
            return f"{name}.webm"
        name = name.split(".")[0]
        if os.path.isfile(f"{name}.mkv"):
            return f"{name}.mkv"
        elif os.path.isfile(f"{name}.mp4"):
            return f"{name}.mp4"
        elif os.path.isfile(f"{name}.mp4.webm"):
            return f"{name}.mp4.webm"

        return name
    except FileNotFoundError as exc:
        return os.path.isfile.splitext[0] + "." + "mp4"


#-----------------Send it to the log channel-----------------------
async def send_doc(bot: Client, m: Message, cc, ka, cc1, count, name, log_channel_id):
    reply = await m.reply_text(f"**Uᴘʟᴏᴀᴅɪɴɢ** » `{name}`\n\n **Bot Made By ʟʊʍɨռǟռȶ✨**")
    time.sleep(1)
    start_time = time.time()
    # Upload the document and capture the message
    message = await m.reply_document(ka, caption=cc1)
    # Capture the file_id of the uploaded document
    file_id = message.document.file_id
    # Send the document to the log channel using file_id
    await bot.send_document(log_channel_id, file_id, caption=cc1)    
    # Increment count
    count += 1
    # Delete the reply message
    await reply.delete(True)
    # Remove the local file
    time.sleep(1)
    os.remove(ka)
    time.sleep(3)

async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, log_channel_id):
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)

    try:
        if thumb == "no":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))
        return

    dur = int(duration(filename))

    try:
        # Send video to user and capture the message
        message = await m.reply_video(filename, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur)
        file_id = message.video.file_id  # Capture the file_id of the uploaded video
    except Exception as e:
        logging.error(e)
        # If sending video fails, send as document and capture the message
        message = await m.reply_document(filename, caption=cc)
        file_id = message.document.file_id  # Capture the file_id of the uploaded document
    
    # Send the video to the log channel using file_id
    try:
        await bot.send_video(log_channel_id, file_id, caption=cc, supports_streaming=True)
    except Exception as e:
        logging.error(f"Failed to send video to log channel: {e}")
        # If sending video fails, send as document using file_id
        await bot.send_document(log_channel_id, file_id, caption=cc)
    
    # Clean up
    os.remove(filename)
    os.remove(f"{filename}.jpg")
