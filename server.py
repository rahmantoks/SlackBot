# custom_http_server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler
from animal import Cat, Dog
import cgi

class CustomRequestHandler(SimpleHTTPRequestHandler):

    # Override POST method
    def do_POST(self):
        # Specify the path where you want to handle POST requests
        if self.path == '/cat':
            self.animal = Cat()
            self.handle_post_request()
        elif self.path == '/dog':
            self.animal = Dog()
            self.handle_post_request()
        # For all other paths, respond with a 404 Not Found
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def handle_post_request(self):
        content_type, _ = cgi.parse_header(self.headers.get('content-type'))
        content_length = int(self.headers.get('content-length'))
        post_data = self.rfile.read(content_length)

        # Handle the POST data here (e.g., save it to a file, process it, etc.)
        # You can replace the following code with your custom logic.
        response_message = f'Received POST data: {post_data.decode()}'

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_message.encode())

if __name__ == '__main__':
    server_address = ('', 80)  # Change the port if needed
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print('Server is running on port 8000...')
    httpd.serve_forever()
