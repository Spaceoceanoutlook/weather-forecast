from flask import Flask, render_template, request
from service import get_temperature

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['user_city']
        forecast = get_temperature(city=city)
        if isinstance(forecast, str):
            return render_template("index.html", error=forecast)
        return render_template("index.html", forecast=forecast)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
