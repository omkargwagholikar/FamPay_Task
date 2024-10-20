from datetime import datetime, timedelta, timezone
from django_apscheduler import util
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import APIKey, FetchHistory, Video, SearchQuery

# To convert naive date time into zone aware date time
from django.utils.timezone import make_aware

# For environment variables
import os
from dotenv import load_dotenv

load_dotenv()

ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_last_update_time():
    try:
        latest_record = FetchHistory.objects.latest("last_fetch_time")
        return latest_record.last_fetch_time.strftime(ISO_DATE_FORMAT)
    except FetchHistory.DoesNotExist:
        video_update_default_time = int(os.getenv("video_update_default_time"))
        n_minutes_before_now = datetime.now() - timedelta(
            minutes=video_update_default_time
        )
        return n_minutes_before_now.strftime(ISO_DATE_FORMAT)


@util.close_old_connections
def get_new_videos_periodic():
    last_update = get_last_update_time()
    print(f"last update at: {last_update}")
    keys = APIKey.objects.filter(is_limit_over=False)
    if len(keys) == 0:
        return "NO KEYS REMAINING"

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
                q=os.getenv("video_search_query"),
                type="video",
                part="snippet",
                maxResults=int(os.getenv("max_video_results")),
                order="date",
                publishedAfter=last_update,
            )
            .execute()
        )
        print(search_response)
        process_response(search_response)

        # temp = {
        #     "kind": "youtube#searchListResponse",
        #     "etag": "5lw3WTrdfPPbKbmbwA3iJQr3ZpI",
        #     "regionCode": "ZZ",
        #     "pageInfo": {"totalResults": 1601, "resultsPerPage": 3},
        #     "items": [
        #         {
        #             "kind": "youtube#searchResult",
        #             "etag": "t-eNITs43S3kAOx_aGYxXAcLozI",
        #             "id": {"kind": "youtube#video", "videoId": "OWkKLUUd3og"},
        #             "snippet": {
        #                 "publishedAt": "2024-10-19T15:53:24Z",
        #                 "channelId": "UCWdhBBk9ElDdYAl4RrMHmwg",
        #                 "title": "Mr Beast😅",
        #                 "description": "",
        #                 "thumbnails": {
        #                     "default": {
        #                         "url": "https://i.ytimg.com/vi/OWkKLUUd3og/default.jpg",
        #                         "width": 120,
        #                         "height": 90,
        #                     },
        #                     "medium": {
        #                         "url": "https://i.ytimg.com/vi/OWkKLUUd3og/mqdefault.jpg",
        #                         "width": 320,
        #                         "height": 180,
        #                     },
        #                     "high": {
        #                         "url": "https://i.ytimg.com/vi/OWkKLUUd3og/hqdefault.jpg",
        #                         "width": 480,
        #                         "height": 360,
        #                     },
        #                 },
        #                 "channelTitle": "AJ ASADUL2003",
        #                 "liveBroadcastContent": "none",
        #                 "publishTime": "2024-10-19T15:53:24Z",
        #             },
        #         },
        #         {
        #             "kind": "youtube#searchResult",
        #             "etag": "kF_s56N25VQa7uXrYzR7bzcbm0A",
        #             "id": {"kind": "youtube#video", "videoId": "jbKpj3zI4qo"},
        #             "snippet": {
        #                 "publishedAt": "2024-10-19T15:52:51Z",
        #                 "channelId": "UCU3WlKoz7w946h9pDp31RsA",
        #                 "title": "Mr Beast Brain Teaser #shorts #brain_teaser #quiz",
        #                 "description": "",
        #                 "thumbnails": {
        #                     "default": {
        #                         "url": "https://i.ytimg.com/vi/jbKpj3zI4qo/default.jpg",
        #                         "width": 120,
        #                         "height": 90,
        #                     },
        #                     "medium": {
        #                         "url": "https://i.ytimg.com/vi/jbKpj3zI4qo/mqdefault.jpg",
        #                         "width": 320,
        #                         "height": 180,
        #                     },
        #                     "high": {
        #                         "url": "https://i.ytimg.com/vi/jbKpj3zI4qo/hqdefault.jpg",
        #                         "width": 480,
        #                         "height": 360,
        #                     },
        #                 },
        #                 "channelTitle": "quiztrivia85",
        #                 "liveBroadcastContent": "none",
        #                 "publishTime": "2024-10-19T15:52:51Z",
        #             },
        #         },
        #         {
        #             "kind": "youtube#searchResult",
        #             "etag": "QeaBlqvxEDBUn6_pHf4XB9oQ0kM",
        #             "id": {"kind": "youtube#video", "videoId": "0jUfSDYJUWg"},
        #             "snippet": {
        #                 "publishedAt": "2024-10-19T15:52:00Z",
        #                 "channelId": "UCqHqK13ulKPh5sLXkN1Cjmw",
        #                 "title": "Will A Basketball Boat Hold My Weight ? | Mr beast #shorts #trending",
        #                 "description": "Will A Basketball Boat Hold My Weight ? | Mr beast #shorts #trending.",
        #                 "thumbnails": {
        #                     "default": {
        #                         "url": "https://i.ytimg.com/vi/0jUfSDYJUWg/default.jpg",
        #                         "width": 120,
        #                         "height": 90,
        #                     },
        #                     "medium": {
        #                         "url": "https://i.ytimg.com/vi/0jUfSDYJUWg/mqdefault.jpg",
        #                         "width": 320,
        #                         "height": 180,
        #                     },
        #                     "high": {
        #                         "url": "https://i.ytimg.com/vi/0jUfSDYJUWg/hqdefault.jpg",
        #                         "width": 480,
        #                         "height": 360,
        #                     },
        #                 },
        #                 "channelTitle": "RGYadavSkb",
        #                 "liveBroadcastContent": "none",
        #                 "publishTime": "2024-10-19T15:52:00Z",
        #             },
        #         },
        #     ],
        # }
        # process_response(temp)

        print("Data fetch successful")

    except HttpError as e:
        if "quotaExceeded" in str(e):
            print(f"Key quota exceeded: {key}")
            print(e)
            key.is_limit_over = True
            key.save()
            return f"Key quota exceeded: {key}"

        else:
            print(f"UNEXPECTED ERROR1: {e}")
            return f"UNEXPECTED ERROR1: {e}"

    except Exception as e:
        print(f"UNEXPECTED ERROR2: {e}")
        return f"UNEXPECTED ERROR2: {e}"

    return "Success"


def process_response(search_response):
    last_video_id = ""
    for search_result in search_response.get("items", []):
        # print(search_result)
        video_id = search_result["id"]["videoId"]

        published_at_given = datetime.strptime(
            search_result["snippet"]["publishedAt"], ISO_DATE_FORMAT
        )
        time_zone_aware_time = make_aware(published_at_given)

        video_data = {
            "video_id": search_result["id"]["videoId"],
            "title": search_result["snippet"]["title"],
            "description": search_result["snippet"]["description"],
            "published_at": time_zone_aware_time,
            "thumbnail_url": str(search_result["snippet"]["thumbnails"]["high"]["url"]),
        }

        Video.objects.update_or_create(video_id=video_id, defaults=video_data)

        try:
            # print(f"Video: {search_result['snippet']['title']}")
            last_video_id = max(video_data["video_id"], last_video_id)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    update_history = FetchHistory(
        last_video_id=last_video_id, last_fetch_time=make_aware(datetime.now())
    )

    update_history.save()


def get_new_videos_querywise(query):
    searchQuery = SearchQuery.objects.get_or_create(query=query)

    last_update = get_last_update_time()
    keys = APIKey.objects.filter(is_limit_over=False)

    if len(keys) == 0:
        return "NO KEYS REMAINING"

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
                q=query,
                type="video",
                part="snippet",
                maxResults=int(os.getenv("max_video_results")),
                order="date",
                publishedAfter=last_update,
            )
            .execute()
        )
        print(search_response)
        process_response(search_response)
        print("Data fetch successful")

    except HttpError as e:
        if "quotaExceeded" in str(e):
            print(f"Key quota exceeded: {key}")
            print(e)
            key.is_limit_over = True
            key.save()
            return f"Key quota exceeded: {key}"

        else:
            print(f"UNEXPECTED ERROR1: {e}")
            return f"UNEXPECTED ERROR1: {e}"

    except Exception as e:
        print(f"UNEXPECTED ERROR2: {e}")
        return f"UNEXPECTED ERROR2: {e}"

    return "Success"
