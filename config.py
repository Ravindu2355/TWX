import os

class Config:
    API_ID = int(os.getenv("apiid", "12345"))
    API_HASH = os.getenv("apihash", "")
    BOT_TOKEN = os.getenv("tk", "")
    CHANNEL_ID = int(os.getenv("channel", "-1001234567890"))

    # Twitter API
    API_URL = "https://x.com/i/api/graphql/jCRhbOzdgOHp6u9H4g2tEg/UserMedia"
    HEADERS = {
        "authorization": os.getenv("TWTk", ""),
        "x-csrf-token": os.getenv("TWCsrf", ""),
        "cookie": os.getenv("TWCookie", ""),
        "accept": "*/*",
        "content-type": "application/json"
    }
    PARAMS = {
        "variables": '{"userId":"1598880214444113920","count":20,"includePromotedContent":false}',
        "features": '{"responsive_web_graphql_timeline_navigation_enabled":true}'
  }
