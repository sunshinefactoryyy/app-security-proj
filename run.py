from app import app
from pathlib import Path
from livereload import Server

if __name__ == '__main__':
    # app.run(debug=True, ssl_context=(Path('./ssl.crt'), Path('./ssl.key')))
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve(port=5000)
