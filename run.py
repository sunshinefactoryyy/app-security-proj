from app import app
from livereload import Server

if __name__ == '__main__':
    # macOS/Linux
    # app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'))
    
    # Windows
    # app.run(debug=True, ssl_context=('.\\ssl.crt', '.\\ssl.key'))
    
    # Auto Reload Browser (Don't Login with Google)
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve()