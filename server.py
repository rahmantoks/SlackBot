# custom_http_server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler
from animal import Cat, Dog
import cgi
import sys
from slack import Slack
from datetime import date
import deepl
import configparser
from urllib.parse import parse_qs

config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
trans = deepl.Translator(config["DEEPL"]["KEY"])
sys.getdefaultencoding()

class CustomRequestHandler(SimpleHTTPRequestHandler):
    # Override POST method
    def do_POST(self):
        # Specify the path where you want to handle POST requests
        if self.path == '/cat':
            self.animal = Cat()
            self.send_response(200)
            self.end_headers()
            self.handle_post_request()

        elif self.path == '/dog':
            self.animal = Dog()
            self.send_response(200)
            self.end_headers()
            self.handle_post_request()

        # For all other paths, respond with a 404 Not Found
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_post_request(self):
        length = int(self.headers.get('content-length'))
        field_data = self.rfile.read(length)
        fields = parse_qs(str(field_data,"UTF-8"))

        print(fields)
        handle_request(fields,self.animal)

def handle_request(params,animal):
    desc_jp = "(以下deepl自動翻訳です)\n\n" + translate(animal.description())
    name_jp  = translate(animal.breedname) + "(" + animal.breedname + ")"

    slack = Slack(params)
    slack.create_payload(name_jp,animal.pic)
    slack.post()

    ## TODO ##
    ## Bot need to be in the channel to see conversation ##
    # slack.create_reply(name_jp,desc_jp)
    # slack.post_reply()

def translate(input):
    result = trans.translate_text(input,target_lang="ja")
    return result.text
        
if __name__ == '__main__':
    server_address = ('', 8000)  # Change the port if needed
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print('Server is running on port 8000...')
    httpd.serve_forever()
