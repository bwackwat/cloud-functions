import requests

def index(request):
    #request_json = request.get_json(silent=True)
    #request_args = request.args

    #if request_json and 'name' in request_json:
    #    name = request_json['name']

    key = None
    username = None
    if request.args and "key" in request.args:
        key = request.args["key"]
    if request.args and "usernmae" in request.args:
        username = request.args["username"]

    if key is None:
        return "403"



    try:
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/channels",
            params={
                "key": key,
                "part": "snippet,contentDetails,statistics",
                "forUsername": username
            },
            headers={
                # "Authorization": "Bearer " + key,
                "Accept": "application/json"
            }
        )
    except Exception as e:
        return str(e)

    return response.text()
