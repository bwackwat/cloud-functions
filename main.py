import requests, json, os

def index(request):
    #request_json = request.get_json(silent=True)
    #request_args = request.args

    #if request_json and 'name' in request_json:
    #    name = request_json['name']

    ytkey = os.environ.get("ytkey")
    mykey = os.environ.get("mykey")
    if ytkey is None:
        return "No YouTube key."
    if mykey is None:
        return "No API key."

    key = None
    username = None
    if request.args and "key" in request.args:
        key = request.args["key"]
    if request.args and "username" in request.args:
        username = request.args["username"]

    if username is None:
        return "No username param."
    if key is None:
        return "No key param."
    if key != mykey:
        return "Bad key."

    channel_url = None
    playlist_url = None
    playlist_id = None
    channel_json = None
    playlist_json = None
    try:
        channel_response = requests.get(
            "https://www.googleapis.com/youtube/v3/channels",
            params={
                "key": ytkey,
                "part": "snippet,contentDetails,statistics,id",
                "forUsername": username
            },
            headers={
                "Accept": "application/json"
            }
        )
        channel_url = channel_response.request.url
        channel_json = channel_response.json()
        playlist_id = channel_json["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        playlist_response = requests.get(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            params={
                "key": ytkey,
                "part": "snippet,contentDetails,status,id",
                "playlistId": playlist_id
            },
            headers={
                "Accept": "application/json"
            }
        )
        playlist_url = playlist_response.request.url
        playlist_json = playlist_response.json()
    except Exception as e:
        return json.dumps(
            {"exception": str(e)},
            indent=4
        )

    jresponse = {
        "channel_url": channel_url,
        "playlist_url": playlist_url,
        "playlist_id": playlist_id,
        "channel_json": channel_json,
        "playlist_json": playlist_json
    }

    return json.dumps(jresponse, indent=4)
