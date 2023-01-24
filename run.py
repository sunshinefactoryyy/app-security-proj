from app import app
from pathlib import Path

if __name__ == '__main__':
    app.run(ssl_context=(Path('./ssl.crt'), Path('./ssl.key')), debug=True,port=8080)