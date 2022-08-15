from app import app, socket_
from pathlib import Path

if __name__ == '__main__':
    socket_.run(app, ssl_context=(Path('./ssl.crt'), Path('./ssl.key')), host='0.0.0.0', port='443')