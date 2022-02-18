#!/usr/local/bin/python3

import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler

import main


class Request:
    args = {}


request = Request

#print(main.index(request))

test_functions = []

for function in test_functions:
    request.args["function"] = function
    response = eval("main." + function)(request)
    print('-' * 40)
    print(response)
    print(('-' * 20) + function + ('-' * 20))


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        request = Request()
        request.headers = {}
        print(urllib.parse.urlparse(self.path).query)
        request.args = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        print(request.args)
        for key in request.args:
            print(request.args[key][0])
            request.args[key] = request.args[key][0]
        print(request.args)
        for header in self.headers:
            request.headers[header] = self.headers.get(header)
        self.wfile.write(bytes("<html><head><title>Data</title></head><body>", "utf-8"))
        self.wfile.write(bytes(main.index(request), "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


httpd = HTTPServer(("", 8080), MyHandler)
try:
    print("Serving on 8080...")
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
