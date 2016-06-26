from flask import Flask, request, jsonify, make_response

from readability.readability import Document
import requests

application = Flask(__name__)


@application.route("/")
def hello():
    id = request.args.get('id', '')
    url = request.args.get('url', '')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safa,ri/537.36',
        'Referer': 'https://news.ycombinator.com/item?id=' + id,
        'Origin': 'https://news.ycombinator.com/item?id=' + id
    }
    try:
        ret = requests.get(url, headers=headers)

        doc = Document(ret.content, url=url)

        result = {
            "url": url,
            "title": doc.short_title(),
            "summary": doc.summary(True)
        }
    except:
        result = {
            "url": url,
            "title": "Error",
            "summary": "<h3>Unable to fetch article's content!</h3>"
        }

    resp = make_response(jsonify(result), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp

if __name__ == "__main__":
    application.run(debug=True, use_reloader=True)
