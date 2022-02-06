from app import app

if __name__ == '__main__':
    # macOS/Linux
    # app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'))
    
    # Windows
    app.run(debug=True, ssl_context=('.\\ssl.crt', '.\\ssl.key'))
