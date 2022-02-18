import secrets, json, random, string, base64, os

import requests, cairosvg

from utility import render, get_object_json, base_key


def view_request(request):
    return render("json.html", json_data=get_object_json(request))


def secret(request):
    length = 64
    if request.args and "length" in request.args:
        arg_length = int(request.args["length"])
        if arg_length < 128:
            length = arg_length
    return secrets.token_urlsafe(length)[:length]


def readable_password(request):
    length = 32
    numbers_index = random.randrange(4)
    numbers = "".join([random.choice(string.digits) for i in range(random.randrange(3) + 2)])

    adjectives = open("static/adjectives.txt", "r").read().split("\n")

    nouns = open("static/nouns.txt", "r").read().split("\n")

    password = [numbers if numbers_index == 0 else random.choice(adjectives),
    numbers if numbers_index == 1 else random.choice(adjectives),
    numbers if numbers_index == 2 else random.choice(nouns),
    numbers if numbers_index == 3 else random.choice(nouns)]

    result = "-".join(password)

    difference = len(result) - length
    if difference > 0:
        return result[:length]

    result += "-" + random.choice(nouns)

    difference = len(result) - length
    if difference > 0:
        return result[:length]

    difference = abs(difference)

    return result + "-" + "".join([random.choice(string.digits) for i in range(difference)])


def captcha(request):
    if request.args and "secret" in request.args:
        secret = request.args["secret"]
        if len(secret) > 10:
            secret = secret[:10]
    else:
        secret = "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(6)])

    size = len(secret)

    svg_s = random.randint(35, 50)
    svg_w = svg_s * size
    svg_h = random.randint(40, 60)

    padding = 5

    svg = ['<svg width="' + str(svg_w + padding) + '" height="' + str(svg_h) + '" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">']

    br = str(random.randint(0, 50))
    bg = str(random.randint(0, 50))
    bb = str(random.randint(0, 50))

    svg.append('<rect width="100%" height="100%" fill="rgb(' + br + ', ' + bg + ', ' + bb + ')"/>')

    for index in range(size):
        r = str(random.randint(50, 100))
        g = str(random.randint(50, 150))
        b = str(random.randint(50, 150))
        rotation = str(random.randint(0, 180))
        skewX = str(random.randint(-25, 25))
        skewY = str(random.randint(-25, 25))
        svg.append(('<rect '
                'fill="rgb(' + r + ', ' + g + ', ' + b + ')" '
                'transform="'
                'skewX(' + skewX + ')'
                'skewY(' + skewY + ')'
                'rotate(' + rotation + ', ' + str((index * svg_s) + padding + svg_s / 2) + ', ' + str((svg_h / 2)) + ')'
                '" '
                'height="' + str(svg_h) + '" '
                'width="' + str(svg_s) + '" '
                'y="' + str(padding) + '" '
                'x="' + str((index * svg_s) + padding) + '"/>'
        ))

    for index, letter in enumerate(secret):
        tr = str(random.randint(100, 255))
        tg = str(random.randint(150, 255))
        tb = str(random.randint(150, 255))
        trotation = str(random.randint(-50, 50))
        tx = (index * svg_s) + svg_s / 2
        ty = svg_h - (svg_h / 3)
        skewX = str(random.randint(-25, 25))
        skewY = "0"
        svg.append(('<text '
                'font-size="' + str(svg_h * 5 / 6) + '" '
                'font-family="Monospace" '
                'font-weight="bold" '
                'fill="rgb(' + tr + ', ' + tg + ', ' + tb + ')" '
                'text-anchor="middle" lengthAdjust="spacing" '
                'textLength="' + str(svg_s / 2) + '" '
                'transform="'
                'skewX(' + skewX + ')'
                'skewY(' + skewY + ')'
                'rotate(' + trotation + ', ' + str(tx + padding) + ', ' + str((svg_h / 2) - padding) + ')'
                '" '
                'y="' + str(ty + padding) + '" '
                'x="' + str(tx) + '"'
                '>' + letter + '</text>'
        ))

    # for index in range(size):
    #     strokw = "1"
    #     svg.append(('<path '
    #     'stroke-width="' + strokw + 'px" '
    #     'd="M ' + str(index * svg_s) + ' ' + str(svg_h / 2) + ' '
    #         'Q ' + str((index * svg_s) + svg_s / 4) + ' ' + str(svg_h * 2) + ', '
    #         '' + str((index * svg_s) + svg_s / 2) + ' 0 '
    #         'Q ' + str((index * svg_s) + svg_s / 2) + ' ' + str(svg_h) + ', '
    #         '' + str((index * svg_s) + svg_s) + ' 0" '
    #         # 'T ' + str((index * svg_s) + svg_s) + ' ' + str(svg_h) + '" '
    #         'stroke="white" fill="none"/>'
    #     ))

    svg.append('<line x1="0" y1="' + str(svg_h / 2) + '" x2="' + str(svg_w + padding) + '" y2="' + str(svg_h / 2) + '" style="stroke:crimson;stroke-width:2"/>')

    svg.append('</svg>')

    cairosvg.svg2png(bytestring="".join(svg))

    base64_captcha_data = base64.b64encode(cairosvg.svg2png(bytestring="".join(svg)))
    
    return "<img src='data:image/png;base64, " + base64_captcha_data.decode("utf-8") + "'/>"


def get_places(request):
    key = None
    if request.args and "key" in request.args:
        key = request.args["key"]
    else:
        return "Key is required."

    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    parameters = {
        "location": "48.859294, 2.347589",
        "radius": "500",
        "sensor": "false",
        "keyword": "hotel",
        "key": key
    }
    response = requests.get(base_url, parameters)
    response = json.loads(response.text)
    response = json.dumps(response, sort_keys=True, indent=4)
    return render("json.html", json_data=response)


def get_amadeus_auth(request):
    key = None
    secret = None
    if request.args and "key" in request.args:
        key = request.args["key"]
    if request.args and "secret" in request.args:
        secret = request.args["secret"]
    if key is None or secret is None:
        return "Bad arguments."

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": key,
        "client_secret": secret
    }

    response = requests.post("https://test.api.amadeus.com/v1/security/oauth2/token",
        headers=headers, data=data)
    response = json.loads(response.text)
    if "access_token" in response:
        return response["access_token"]
    response = json.dumps(response, sort_keys=True, indent=4)
    return response


def get_amadeus_hotels(request):
    access_token = None
    city_code = "SAN"
    if request.args and "access_token" in request.args:
        access_token = request.args["access_token"]
    else:
        return "No token argument."
    if request.args and "cityCode" in request.args:
        city_code = request.args["cityCode"]

    headers = {
        "Authorization": "Bearer " + access_token
    }
    params = {
        "cityCode": city_code,
        "roomQuantity": "1",
        "adults": "1",
        "radius": "300",
        "radiusUnit": "mi",
        "paymentPolicy": "NONE",
        "includeClosed": "false",
        "bestRateOnly": "true",
        "view": "FULL",
        "sort": "PRICE"
    }

    response = requests.get("https://test.api.amadeus.com/v2/shopping/hotel-offers?cityCode=SAN&roomQuantity=1&adults=2&radius=300&radiusUnit=KM&paymentPolicy=NONE&includeClosed=false&bestRateOnly=true&view=FULL&sort=NONE",
    headers=headers)
    response = json.loads(response.text)

    if "errors" in response and "title" in response.errors and response.errors["title"] == "Access token expired":
        headers["Authorization"] = "Bearer " + get_amadeus_auth(request)

    response = json.dumps(response, sort_keys=True, indent=4)
    return render("json.html", json_data=response)


functions = [
    "get_places",
    "view_request",
    "secret",
    "readable_password",
    "captcha",
    "get_amadeus_auth",
    "get_amadeus_hotels"
]


def index(request):
    if (not request.args and "jph2cf_key" not in request.args) or request.args["jph2cf_key"] != base_key:
        return 0
    if request.args and "function" in request.args and request.args["function"] in functions:
        return eval(request.args["function"])(request)
    return render("index.html", functions=functions)
