from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from config import PORT


class Handler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is running!")

  def do_HEAD(self):
    self.send_response(200)
    self.end_headers()


def start_http_server():
  server = HTTPServer(("", PORT), Handler)
  threading.Thread(target=server.serve_forever, daemon=True).start()
