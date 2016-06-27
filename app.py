from flask import Flask, request, jsonify, make_response
from werkzeug.contrib.cache import MemcachedCache

from readability.readability import Document
import requests

application = Flask(__name__)

cache = MemcachedCache(['memcache:11211'])


@application.route("/")
def hello():
    id = request.args.get('id', '')
    url = request.args.get('url', '')

    result = cache.get(id)
    if result is None:
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
        cache.set(id, result)

    resp = make_response(jsonify(result), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp

if __name__ == "__main__":
    application.run(debug=False, use_reloader=False)
