import os
from googleapiclient.discovery import build

def l_env(filepath=".env"):
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            os.environ[key] = value

l_env()

yt_api = os.environ.get("YouTube_API")

yt = build("youtube", "v3", developerKey=yt_api)
handle = input("Enter the YouTube channel handle (with or without @): ").lstrip('@')

search_response = yt.search().list(
        q = handle,
        part = "snippet",
        type = "channel",
        maxResults = 1
        ).execute()

channel_id = search_response['items'][0]['snippet']['channelId']
print("Channel ID: ", channel_id)

req = yt.channels().list(
            part = "statisitcs",
            id = channel_id
        )

pl_req = yt.playlists().list(
        part = "snippet, contentDetails",
        channelId = channel_id,
        maxResults = 10
        )

res_pl = pl_req.execute()
res_ch = req.execute()

print(res_ch)
print(res_ch)



