import os
from dotenv import load_dotenv
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

load_dotenv()

def keyword2vid(keyword: str):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")# STRANGER DANGER

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=500,
        order = "date",
        q=keyword,
        type="video"
    )
    response = request.execute()
    # response = response.json()
    
    print(f"keyword '{keyword}' to {len(response["items"])} vids")
    for item in response["items"]:
        # print(f"{item["id"]["videoId"]}")
        # print(f"    {item["snippet"]["title"]}")
        # print(f"        {item["snippet"]["channelId"]}")
        # print(f"            {item["snippet"]["channelTitle"]}")
        yield {
            "video": {
                "id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
            },
            "channel": {
                "id": item["snippet"]["channelId"],
                "title": item["snippet"]["channelTitle"],
            },
            "date": item["snippet"]["publishTime"],
        }


if __name__ == "__main__":
    # print(next(keyword2vid("蔡英文")))
    for item in keyword2vid("蔡英文"):
        print(item)