import os
import asyncio
from pyrogram import Client, filters
from config import Config
from twitter_api import fetch_media
from downloader import download_file
from uploader import upload_to_channel

app = Client("twitter_dl", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("👋 Hello! I can auto-download videos from X/Twitter and upload them here.")


@app.on_message(filters.command("fetch"))
async def fetch_and_upload(_, message):
    await message.reply_text("🔍 Fetching videos...")
    videos = fetch_media()

    if not videos:
        await message.reply_text("❌ No videos found.")
        return

    for idx, url in enumerate(videos, 1):
        filename = f"video_{idx}.mp4"

        msg = await message.reply_text(f"⬇️ Downloading {idx}/{len(videos)}...")

        # progress callback for download
        def download_progress(current, total, percent, elapsed):
            asyncio.run_coroutine_threadsafe(
                msg.edit_text(f"⬇️ Downloading {idx}/{len(videos)}\n"
                              f"{percent:.2f}% ({current//1024//1024}MB/{total//1024//1024}MB)\n"
                              f"⏱ Elapsed: {int(elapsed)}s"),
                app.loop
            )

        download_file(url, filename, progress_callback=download_progress)

        await msg.edit_text(f"⬆️ Uploading {idx}/{len(videos)}...")

        async def upload_progress(current, total, percent, elapsed):
            await msg.edit_text(f"⬆️ Uploading {idx}/{len(videos)}\n"
                                f"{percent:.2f}% ({current//1024//1024}MB/{total//1024//1024}MB)\n"
                                f"⏱ Elapsed: {int(elapsed)}s")

        await upload_to_channel(app, filename, Config.CHANNEL_ID, progress_callback=upload_progress)

        os.remove(filename)
        await msg.edit_text(f"✅ Uploaded {idx}/{len(videos)}")


if __name__ == "__main__":
    app.run()
