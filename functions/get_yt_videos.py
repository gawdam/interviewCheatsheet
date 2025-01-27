from googleapiclient.discovery import build


def replace_youtube_videos_with_links(json_data, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)

    for concept in json_data.get("concepts_revision", []):
        search_term = concept.get("youtube_video")
        if search_term:
            try:
                # Search YouTube for the video
                request = youtube.search().list(
                    q=search_term,
                    part="snippet",
                    type="video",
                    maxResults=1,
                    # order="relevance"
                )
                response = request.execute()
                print(response)
                # Replace the `youtube_video` title with a valid YouTube link
                if response.get("items"):
                    video_id = response["items"][0]["id"]["videoId"]
                    youtube_link = f"{video_id}"
                    concept["youtube_video"] = youtube_link
                else:
                    # If no video is found, set a placeholder link
                    concept["youtube_video"] = "No valid video found for this topic."
            except Exception as e:
                # Handle API errors gracefully
                concept["youtube_video"] = f"Error fetching video: {str(e)}"

    return json_data