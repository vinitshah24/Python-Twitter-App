import os
import json
from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'merky'

blueprint = make_twitter_blueprint(
    api_key=os.getenv('FLASK_TWITTER_API_KEY'),
    api_secret=os.getenv('FLASK_TWITTER_API_SECRET'),
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok
    return "{screen_name}".format(screen_name=resp.json())


if __name__ == "__main__":
    app.run(debug=True)
