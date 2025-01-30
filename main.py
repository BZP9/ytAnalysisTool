import os
import googleapiclient.discovery
import csv
from datetime import datetime

def readVidList(path: str):
    with open(path,'r',encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            getComments(row["vid"])

def getComments(id: str):
    saveFilePath = r'C:\Users\liaol\OneDrive\desktop\BoogerAids\ytCommentExact'

    if os.path.exists(fr'{saveFilePath}/{id}.csv'):
        print(f'skip {id}')
        return

    print(f'get {id}')
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAHLQBcFDVTF9hY1D5AWxOIDIBF48vRM5A" # STRANGER DANGER

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    NPT = None
    comments = []
    
    try:
        while True:
            if NPT == None:
                request = youtube.commentThreads().list(
                    part="snippet",
                    maxResults=100,
                    order="time",
                    videoId=id,
                )
            else:
                request = youtube.commentThreads().list(
                    part="snippet",
                    maxResults=100,
                    order="time",
                    videoId=id,
                    pageToken = NPT
                )

            response = request.execute()

            NPT = response.get('nextPageToken') if response.get('nextPageToken') else None
            # print(NPT)


            comments += [
                {
                    "cHandle": item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "publishTime": int(datetime.strptime(item['snippet']['topLevelComment']['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").timestamp())
                }
                for item in response['items']
            ]

            if not NPT:
                break
        
    except Exception as e:
        print(f"發生錯誤: {e}")
    
    if(len(comments) > 0):

        csv_file = f"{id}.csv"
        with open(fr'{saveFilePath}/{csv_file}', mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["cHandle", "publishTime"])
            writer.writeheader()
            writer.writerows(comments)

        print(len(comments))
    else:
        print(f"{id} is busted")

if __name__ == '__main__':
    getComments('B_KSH6w-gps')
    # readVidList(r"C:\Users\liaol\OneDrive\desktop\BoogerAids\ytCommentExact\___vidList.csv")
    print('finish')