from flask import Flask, render_template, request
from service import get_temperature, get_time

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['user_city']
        forecast, country, population = get_temperature(city=city)
        population = f"{population: _}".replace("_", " ")
        context = {"country": country, "population": population, "time": get_time(), "city": city, "forecast": forecast}
        if isinstance(forecast, str):
            return render_template("index.html", **context)
        return render_template("index.html", **context)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
