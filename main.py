from flask import Flask, render_template
import requests
import os

# App Settings
app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
ENDPOINT = "https://api-tokyochallenge.odpt.org/api/v4/"

# Request the data from API
data_type = "odpt:TrainInformation?"
params = {
    "acl:consumerKey": API_KEY
}
response = requests.get(ENDPOINT + data_type, params=params)
data = response.json()


@app.route("/")
def home():
    time = [information['dc:date'].split('T')[1].split('+')[0] for information in data]
    train_status = [information['odpt:trainInformationText']['ja'] for information in data]
    railways = [information['owl:sameAs'].split(':')[1] for information in data]
    return render_template("index.html", time=time, train_status=train_status, railways=railways)


if __name__ == "__main__":
    app.run(debug=True)