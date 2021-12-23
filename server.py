from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cusInfo')
def cusInfo():
    return render_template('cus_info.html')

@app.route('/cusReq')
def cusReq():
    return render_template('cusReq.html')
    
if __name__ == '__main__':
    app.run(debug=True)