import os
import requests
import json

backend_url = os.getenv('backend_url', 'http://localhost:3030')
sentiment_analyzer_url = os.getenv('https://sentianalyzer.28zsfifyh4is.us-south.codeengine.appdomain.cloud/', 'http://localhost:5050/')

def get_request(endpoint, **kwargs):
    params = ""

    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = backend_url + endpoint

    if params:
        request_url += "?" + params

    print("GET from:", request_url)

    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Network exception:", e)
        return None


def analyze_review_sentiments(text):
    try:
        response = requests.get(sentiment_analyzer_url + "analyze/" + text)
        return response.json()
    except Exception as e:
        print("Sentiment error:", e)
        return {"sentiment": "neutral"}