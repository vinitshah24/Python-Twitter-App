import os
from dotenv import load_dotenv
from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

# Load env variables
env_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '.env')
)
load_dotenv(env_file)

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key=os.environ.get(
                               'FLASK_TWITTER_API_KEY'),
                           consumer_secret=os.environ.get("FLASK_TWITTER_API_SECRET"))


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    access_token = access_token[0]
    return render_template('index.html')


@app.route('/login')
def login():
    return twitter.authorize(
        callback=url_for('oauth_authorized',
                         next=request.args.get('next')
                         or request.referrer or None))


@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@app.route('/flask_oauth_app-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    access_token = resp['oauth_token']
    print(session)
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
