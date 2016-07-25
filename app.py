from flask import Flask, request, jsonify, make_response
from werkzeug.contrib.cache import MemcachedCache

#from readability.readability import Document
#import requests
from readability import ParserClient

application = Flask(__name__)

cache = MemcachedCache(['memcache:11211'])
parser_client = ParserClient()

@application.route("/")
def hello():
    id = request.args.get('id', '')
    url = request.args.get('url', '')



    result = cache.get(id)
    if result is None:
        try:
            parser_response = parser_client.get_article(url)
            result = parser_response.json()
        except:
            result = {
                "title": "Error",
                "content": "<h3>Unable to fetch article's content!</h3>",
            }
        result['summary'] = '<h3>You are using the out-dated Hacker News app, please update to latest version!</h3>'
        cache.set(id, result)

    resp = make_response(jsonify(result), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp

if __name__ == "__main__":
    application.run(debug=False, use_reloader=False)
