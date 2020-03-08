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

    try:
        channel_response = requests.get(
            "https://www.googleapis.com/youtube/v3/channels",
            params={
                "key": ytkey,
                "part": "snippet,contentDetails,statistics",
                "forUsername": username
            },
            headers={
                "Accept": "application/json"
            }
        )
        channel_json = channel_response.json()
        next_playlist = channel_json["data"]["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        playlist_response = requests.get(
            "https://www.googleapis.com/youtube/v3/playlists",
            params={
                "key": ytkey,
                "part": "snippet,contentDetails,status,player,id",
                "id": next_playlist
            },
            headers={
                "Accept": "application/json"
            }
        )
    except Exception as e:
        return json.dumps(
            {"exception": str(e)},
            indent=4
        )

    jresponse = {
        "channel_url": channel_response.request.url,
        "playlist_url": playlist_response.request.url,
        "playlist_id": next_playlist,
        "channel_json": channel_json,
        "playlist_json": playlist_response.json()
    }

    return json.dumps(jresponse, indent=4)
