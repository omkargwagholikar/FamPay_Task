from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import redis
import requests
from .models import APIKey, FetchHistory, Video

ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_last_update_time():
    try:
        latest_record = FetchHistory.objects.latest("last_fetch_time")
        return latest_record.last_fetch_time.strftime(ISO_DATE_FORMAT)
    except FetchHistory.DoesNotExist:  
        date = datetime(2024, 10, 19)      
        return date.strftime(ISO_DATE_FORMAT)

def get_new_videos():
    while True:
        last_update = get_last_update_time()
        print(f"last update at: {last_update}")
        keys = APIKey.objects.filter(is_limit_over=False)
        if len(keys) == 0:
            print("NO KEYS REMAINING")
            return
        try:
            key = keys[0]
            print(f"Using key: {key}")
            youtube_object = build(
                    YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=key,
            )

            search_response = (
                    youtube_object.search()
                    .list(
                        q="mr beast",
                        type="video",
                        part="snippet",
                        maxResults=5,
                        order="date",
                        publishedAfter= last_update
                    )
                    .execute()
            )
            process_response(search_response)
            print("Data fetch successful")

            break
            
        except HttpError as e:
            if "quotaExceeded" in str(e):
                print(f"Key quota exceeded: {key}")
                print(e)
                key.is_limit_over = True
                key.save()
            else:
                print(f"UNEXPECTED ERROR1: {e}")
        except Exception as e:
            print(f"UNEXPECTED ERROR2: {e}")

def process_response(search_response):
    last_video_id = None
    for search_result in search_response.get("items", []):
        print(search_result)
        video_data = Video(
            video_id = search_result["id"]["videoId"],
            title = search_result["snippet"]["title"],
            description = search_result["snippet"]["description"],
            published_at = datetime.strptime(
                search_result["snippet"]["publishedAt"], ISO_DATE_FORMAT
            ),
            thumbnail_url =str(search_result["snippet"]
                           ["thumbnails"]["high"]["url"]),
        )

        video_data.save()
        try:
            print(f"Video: {search_result['snippet']['title']}")
            last_video_id = max(video_data.video_id, last_video_id)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    update_history = FetchHistory(
        last_video_id = last_video_id,
        last_fetch_time = datetime.now()
    )
    
    update_history.save()
