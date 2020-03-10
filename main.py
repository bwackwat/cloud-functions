#!/usr/local/bin/python3

import requests, json, os, sys, json

response = {}
global ytkey
ytkey = os.environ.get("ytkey")
global mykey
mykey = os.environ.get("mykey")


def get_videos(ids):
    response = {}
    global ytkey
    videos_response = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "key": ytkey,
            "part": "recordingDetails,snippet,contentDetails,statistics,id,topicDetails,liveStreamingDetails",
            "id": ids
        },
        headers={
            "Accept": "application/json"
        }
    )
    # response["videos_url"] = videos_response.request.url
    rjson = videos_response.json()
    #response["videos_json"] = videos_response.json()
    response = []
    for video in rjson["items"]:
        response["data"].append({
            "id": video["id"],
            "title": video["snippet"]["title"],
            "statistics": video["statistics"]
        })
    return response


def index(request):
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


    global response

    #data1_ids = ",".join([data1[i][0] for i in range(10)])
    data1_ids = ",".join([data1[i][0] for i in range(50)])
    #response["ids"] = data1[0][0]
    #data1_ids = ",".join([data[0] for data in data1])
    #response["videos1"] = get_videos(data1[0][0])
    response["result"] = get_videos(data1_ids)

    try:
        # channel_response = requests.get(e
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
        pass
    except Exception as e:
        response["exception"] = str(vars(e))

    return "<pre>" + json.dumps(response, indent=4) + "</pre>"


class Request():
    def __init__(self, args):
        self.args = args


if __name__ == "__main__":
    ytkey = sys.argv[3]
    mykey = sys.argv[1]
    print(json.dumps(index(Request({
        "key": sys.argv[1],
        "username": sys.argv[2]
    }))))

