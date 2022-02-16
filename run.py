from app import app
from pathlib import Path

if __name__ == '__main__':
    app.run(debug=True,ssl_context=(Path('./ssl.crt'), Path('./ssl.key')))