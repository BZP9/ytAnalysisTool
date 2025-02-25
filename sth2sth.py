import os
from dotenv import load_dotenv
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime

load_dotenv()
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")# STRANGER DANGER
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

def keyword2vid(keyword: str):
    request = youtube.search().list(
        part="snippet",
        maxResults=100,
        order = "date",
        q=keyword,
        type="video",
        topicId="/m/05qt0",
    )
    response = request.execute()
    # response = response.json()
    
    print(f"keyword '{keyword}' to {len(response["items"])} vids")
    for item in response["items"]:
        thing = {
            "videoId": item["id"]["videoId"],
            "videoTitle": item["snippet"]["title"],
            "channelId": item["snippet"]["channelId"],
            "channelTitle": item["snippet"]["channelTitle"],
        }
        yield thing

def vid2comment(vid):
    NEXT_PAGE_TOKEN = None
    try:
        while True:
            if NEXT_PAGE_TOKEN == None:
                request = youtube.commentThreads().list(
                    part="snippet",
                    maxResults=100,
                    order="time",
                    videoId=vid,
                )
            else:
                request = youtube.commentThreads().list(
                    part="snippet",
                    maxResults=100,
                    order="time",
                    videoId=vid,
                    pageToken = NEXT_PAGE_TOKEN,
                )
            response = request.execute()
            NEXT_PAGE_TOKEN = response.get("nextPageToken", None)
            print(f"vid '{vid}' to {len(response["items"])} comments")
            for item in response["items"]:
                comment = {
                    "commentId": item["id"],
                    "textOriginal": item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                    "authorDisplayName": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    "videoId": item["snippet"]["topLevelComment"]["snippet"]["videoId"],  # Fix videoId path
                    "publishedAt": datetimeConvert(item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]),
                }
                # print(comment)
                yield comment
            
            if(NEXT_PAGE_TOKEN == None):
                break

    except Exception as ex:
        print(ex)
        
def vid2info(vid):
    print(vid)
    request = youtube.videos().list(
        part="snippet,statistics",
        id=vid,
    )
    response = request.execute()
    # response = request.execute()["items"][0]
    info = {
        "videoId": vid,
        "publishedAt": datetimeConvert(),
        "viewCount": -1,
        "likeCount": -1,
        "commentCount": -1
    }
    if len(response["items"]) == 0:
        return info
    response = response["items"][0]
    info = {
        "videoId": response["id"],
        "publishedAt": datetimeConvert(response["snippet"]["publishedAt"]),
        "viewCount": response["statistics"].get("viewCount", 0),
        "likeCount": response["statistics"].get("likeCount", 0),
        "commentCount": response["statistics"].get("commentCount", 0)
    }
    return info

def datetimeConvert(date=None):
    if date is None:
        date = "1970-01-01T00:00:00Z"  # Default fallback value
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

if __name__ == "__main__":
    # for item in keyword2vid("蔡英文"):
    #     print(item)
    # for item in vid2comment("tREINnJZMJ4"):
    #     print(item)
    print(vid2info("60gjxMId4Qk"))