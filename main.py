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


    data1 = []
    with open("data1.csv", "r") as f:
        for line in f.readlines():
            ldata = line.split(",")
            # ID, guest in video, season-episode
            data1.append([ldata[0], ldata[1], ldata[2]])
    data2 = []
    with open("data2.csv", "r") as f:
        for line in f.readlines():
            ldata = line.split(",")
            # ID
            data2.append([ldata[0], ldata[1]])
    data3 = []
    with open("data3.csv", "r") as f:
        for line in f.readlines():
            ldata = line.split(",")
            # IDm, season #, [0, next names are people in thumbnail][1 quest in video]
            data3.append([ldata[0], ldata[1], ldata[2], ldata[3]])

    jresponse = {}

    try:
        data1_ids = ",".join([data1[i] for i in range(10)])
        jresponse["ids"] = data1[0][0]
        #data1_ids = ",".join([data[0] for data in data1])
        videos_response = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "key": ytkey,
                "part": "recordingDetails,snippet,contentDetails,statistics,id,topicDetails,liveStreamingDetails",
                "id": data1_ids
            },
            headers={
                "Accept": "application/json"
            }
        )
        jresponse["videos1_url"] = videos_response.request.url
        jresponse["videos1_json"] = videos_response.json()
        videos_response = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "key": ytkey,
                "part": "recordingDetails,snippet,contentDetails,statistics,id,topicDetails,liveStreamingDetails",
                "id": data1_ids
            },
            headers={
                "Accept": "application/json"
            }
        )
        jresponse["videos2_url"] = videos_response.request.url
        jresponse["videos2_json"] = videos_response.json()
        # channel_response = requests.get(
        #     "https://www.googleapis.com/youtube/v3/channels",
        #     params={
        #         "key": ytkey,
        #         "part": "snippet,contentDetails,statistics,id",
        #         "forUsername": username
        #     },
        #     headers={
        #         "Accept": "application/json"
        #     }
        # )
        # channel_url = channel_response.request.url
        # channel_json = channel_response.json()
        # playlist_id = channel_json["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        # playlist_response = requests.get(
        #     "https://www.googleapis.com/youtube/v3/playlistItems",
        #     params={
        #         "key": ytkey,
        #         "part": "snippet,contentDetails,status,id",
        #         "playlistId": playlist_id
        #     },
        #     headers={
        #         "Accept": "application/json"
        #     }
        # )
        # playlist_url = playlist_response.request.url
        # playlist_json = playlist_response.json()

    except Exception as e:
        jresponse["exception"] = str(vars(e))

    return "<pre>" + json.dumps(jresponse, indent=4) + "</pre>"
