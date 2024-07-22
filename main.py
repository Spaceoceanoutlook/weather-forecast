from flask import Flask, render_template, request
from service import get_temperature

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['user_city']
        temp = get_temperature(city_name=data)
        return render_template("index.html", temp=temp)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
