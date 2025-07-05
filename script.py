import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import sqlite3
import threading

# Database setup
conn = sqlite3.connect("messages.db", check_same_thread=False)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY)')
cur.execute('''CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    recipient TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()

# Thread lock for DB
lock = threading.Lock()

# Simple web server
class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        data = json.loads(self.rfile.read(length))

        if self.path == '/login':
            email = data.get('email')
            if not email:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Email required'}).encode())
                return
            with lock:
                cur.execute('INSERT OR IGNORE INTO users (email) VALUES (?)', (email,))
                conn.commit()
            self._set_headers()
            self.wfile.write(json.dumps({'message': f'Logged in as {email}'}).encode())

        elif self.path == '/send':
            sender = data.get('sender')
            recipient = data.get('recipient')
            content = data.get('content')
            if not all([sender, recipient, content]):
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Missing fields'}).encode())
                return
            with lock:
                cur.execute('INSERT INTO messages (sender, recipient, content) VALUES (?, ?, ?)',
                            (sender, recipient, content))
                conn.commit()
            self._set_headers()
            self.wfile.write(json.dumps({'message': 'Message sent'}).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/messages':
            query = parse_qs(parsed.query)
            user1 = query.get('user1', [None])[0]
            user2 = query.get('user2', [None])[0]

            if not all([user1, user2]):
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Missing user1 or user2'}).encode())
                return

            with lock:
                cur.execute('''SELECT sender, recipient, content, timestamp FROM messages
                               WHERE (sender= gavinmd.cornelius@gmail.com AND recipient=trisanth.vu@gmail.com ) OR (sender=gavinmd.cornelius@gmail.com AND recipient=trisanth.vu@gmail.com)
                               ORDER BY timestamp''', (user1, user2, user2, user1))
                messages = cur.fetchall()

            self._set_headers()
            self.wfile.write(json.dumps([
                {'from': s, 'to': r, 'content': c, 'timestamp': t}
                for s, r, c, t in messages
            ]).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

# Run server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    print(f'Server running on http://localhost:{port}')
    server = server_class(('', port), handler_class)
    server.serve_forever()

if __name__ == '__main__':
    run()
