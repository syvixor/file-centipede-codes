from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

TARGET_URL = "https://raw.githubusercontent.com/filecxx/FileCentipede/refs/heads/main/en_US/activation_code.html"


def get_activation_codes():
    response = requests.get(TARGET_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    codes_pre = soup.find("pre", id="codes")
    if not codes_pre:
        return []

    lines = [line.strip() for line in codes_pre.get_text().splitlines() if line.strip()]

    results = []

    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            results.append({
                "dateRange": lines[i],
                "activationCode": lines[i + 1]
            })

    return results


@app.route("/")
def home():
    data = get_activation_codes()
    return render_template("index.html", data=data)