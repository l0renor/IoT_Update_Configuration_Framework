import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8000


def run_server():
    directory = os.path.join(os.getcwd(), 'tufrepo')
    os.chdir(directory)  # change to the dir which should be served
    httpd = HTTPServer(('127.0.0.1', PORT), SimpleHTTPRequestHandler)
    print("serving at port: " + str(PORT))
    httpd.serve_forever()


if __name__ == '__main__':
    print(os.getcwd())
    run_server()
