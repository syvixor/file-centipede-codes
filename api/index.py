from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

TARGET_URL = "https://raw.githubusercontent.com/filecxx/FileCentipede/refs/heads/main/en_US/activation_code.html"


def format_date_range(date_range_str):
    """Convert YYYY-MM-DD HH:MM:SS - YYYY-MM-DD HH:MM:SS to MM/DD/YYYY - MM/DD/YYYY"""
    pattern = r'(\d{4})-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2} - (\d{4})-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}'
    match = re.match(pattern, date_range_str)
    if match:
        start_month, start_day, start_year = match.group(2), match.group(3), match.group(1)
        end_month, end_day, end_year = match.group(5), match.group(6), match.group(4)
        return f"{start_month}/{start_day}/{start_year} - {end_month}/{end_day}/{end_year}"
    return date_range_str


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
                "dateRange": format_date_range(lines[i]),
                "activationCode": lines[i + 1]
            })

    return results


@app.route("/")
def home():
    data = get_activation_codes()
    return render_template("index.html", data=data)