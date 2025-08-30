import asyncio
import os
import time
from pyrogram.errors import FloodWait

async def upload_to_channel(app, file_path, chat_id, progress_callback=None):
    """Upload file to Telegram with progress updates"""
    start = time.time()
    last_update = start

    async def progress(current, total):
        nonlocal last_update
        now = time.time()
        if now - last_update >= 10:  # update every 10s
            percent = (current / total) * 100 if total else 0
            if progress_callback:
                await progress_callback(current, total, percent, now - start)
            last_update = now

    try:
        await app.send_video(
            chat_id=chat_id,
            video=file_path,
            caption=os.path.basename(file_path),
            progress=progress
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await upload_to_channel(app, file_path, chat_id, progress_callback)
