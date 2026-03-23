import json
import os
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 3000
HISTORY_FILE = 'history.json'

class CalculatorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='public', **kwargs)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        if self.path == '/history':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if not os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'w') as f:
                    json.dump([], f)
                    
            try:
                with open(HISTORY_FILE, 'r') as f:
                    data = f.read()
                self.wfile.write(data.encode('utf-8'))
            except Exception as e:
                self.wfile.write(b'[]')
        else:
            # Serve static files from public directory
            super().do_GET()

    def do_POST(self):
        if self.path == '/calculate':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                expression = payload.get('expression')
                result = payload.get('result')
                
                if expression is None or result is None:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing data'}).encode('utf-8'))
                    return
                
                # Load history
                if not os.path.exists(HISTORY_FILE):
                    history = []
                else:
                    with open(HISTORY_FILE, 'r') as f:
                        try:
                            history = json.load(f)
                        except:
                            history = []
                
                import time
                new_entry = {
                    'id': int(time.time() * 1000),
                    'expression': expression,
                    'result': "{:.2f}".format(float(result)),
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S%z')
                }
                
                history.insert(0, new_entry)
                
                with open(HISTORY_FILE, 'w') as f:
                    json.dump(history, f, indent=2)
                    
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(new_entry).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=CalculatorHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    run()
