
from os import urandom
from flask import Flask, redirect, request
from apis import blueprint as api, API_BASE
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.secret_key = urandom(24)
app.wsgi_app = ProxyFix(app.wsgi_app)

# register apis
app.register_blueprint(api, url_prefix=API_BASE)


@app.route("/", methods=["GET"])
def home():
    api_home = "{}/{}".format(request.url_root, API_BASE)
    return redirect(api_home)


if __name__ == '__main__':
    app.run(debug=True)
