from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin -> °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})

    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/github-commits/')
def github_commits():
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw = response.read()
    commits_json = json.loads(raw.decode('utf-8'))

    minutes_list = []
    for c in commits_json:
        date_str = c.get('commit', {}).get('author', {}).get('date')
        if date_str:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(dt.minute)

    return jsonify(results=minutes_list)

@app.route("/commits/")
def commits():
    return render_template("commits.html")


if __name__ == "__main__":
    app.run(debug=True)
