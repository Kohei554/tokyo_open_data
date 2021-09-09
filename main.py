from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests
import os

# App Settings
app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
ENDPOINT = "https://api-tokyochallenge.odpt.org/api/v4/"
Bootstrap(app)

# Request the data from API
data_type = "odpt:TrainInformation?"
params = {
    "acl:consumerKey": API_KEY
}
response = requests.get(ENDPOINT + data_type, params=params)
data = response.json()


@app.route("/")
def home():
    railways = [information['owl:sameAs'].split(':')[1].split(".") for information in data]
    # operators = [railway[0] for railway in railways]
    railways = [" ".join(railway) if len(railway) != 1 else railway[0] for railway in railways]
    train_status = [information['odpt:trainInformationText']['ja'] for information in data]
    time = [":".join(information['dc:date'].split('T')[1].split('+')[0].split(":")[:2]) for information in data]
    return render_template("index.html", railways=railways, train_status=train_status, time=time)


if __name__ == "__main__":
    app.run(debug=True)


