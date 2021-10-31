from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/request")
def request():
    return render_template("request.html", active="request")

@app.route("/about")
def about():
    return render_template("about.html", active="about")

@app.route("/tracking")
def tracking():
    return render_template("tracking.html", active="tracking")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html", active="feedback")

if __name__ == "__main__":
    app.run(debug=True)