from googleapiclient.discovery import build

def replace_youtube_videos_with_links(json_data, api_key):
    json_data_changed = json_data
    youtube = build("youtube", "v3", developerKey=api_key)

    for concept in json_data_changed.get("concepts_revision", []):
        search_term = concept.get("yt_search_query")
        if search_term:
            try:
                # Search YouTube for the video, requesting only the videoId
                request = youtube.search().list(
                    q=search_term,
                    part="id",  # Request only the ID part
                    type="video",
                    maxResults=1,
                )
                response = request.execute()

                # Extract and store the video ID
                if response.get("items"):
                    video_id = response["items"][0]["id"]["videoId"]
                    concept["yt_search_query"] = video_id  # Or concept["youtube_video"] if you prefer
                else:
                    concept["yt_search_query"] = "No valid video found for this topic." # Or concept["youtube_video"]
            except Exception as e:
                concept["yt_search_query"] = f"Error fetching video: {str(e)}" # Or concept["youtube_video"]

    return json_data_changed