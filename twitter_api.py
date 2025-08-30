import requests
from config import Config

def fetch_media():
    """Fetch media JSON from Twitter/X and return best video URLs"""
    r = requests.get(Config.API_URL, headers=Config.HEADERS, params=Config.PARAMS)
    r.raise_for_status()
    data = r.json()
    videos = []
    for entry in data.get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get("timeline", {}).get("instructions", []):
        for item in entry.get("entries", []):
            content = item.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
            media = content.get("legacy", {}).get("extended_entities", {}).get("media", [])
            for m in media:
                if m.get("type") == "video":
                    variants = m.get("video_info", {}).get("variants", [])
                    mp4s = [v for v in variants if "bitrate" in v and v["content_type"] == "video/mp4"]
                    if mp4s:
                        best = sorted(mp4s, key=lambda x: x["bitrate"], reverse=True)[0]
                        videos.append(best["url"])
    return videos
