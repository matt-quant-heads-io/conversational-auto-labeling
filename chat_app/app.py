from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__, template_folder="./")
context_set = ""

response = []  # A list that will store the conversation


@app.route("/", methods=["GET"])
def index():
    response.clear()
    return render_template("index.html", val="")


@app.route("/msg", methods=["POST"])
def msg():
    val = str(request.form["text"])

    data = json.dumps({"sender": "Rasa", "message": val})

    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    res = requests.post(
        "http://localhost:5005/webhooks/rest/webhook", data=data, headers=headers
    )

    if not val or val[0] == "/":
        return render_template("index.html", val=response)
    else:
        res = res.json()
        message = ""
        response.append(val)
        for x in res:
            payload = list(without_keys(x, "recipient_id").values())
            message = message + "  " + str(payload[0])
        response.append(message)
        return render_template("index.html", val=response)


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5008)
