from app import app
from threading import Thread
from os import system

def run():
    # macOS/Linux
    app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'), use_reloader=False)
    
    # Windows
    # app.run(debug=True, ssl_context=('.\\ssl.crt', '.\\ssl.key', use_reloader=False))
    
def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()
    system("npm run dev")