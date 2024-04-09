from flask import Flask, render_template, redirect, request, session
from requests_oauthlib import OAuth1Session
from instagram.client import InstagramAPI
import praw
import facebook

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Dummy user database
users = {
    'user': 'password'  # Store hashed passwords in production
}

# Social media API credentials
twitter_api_key = 'myMiO0XD0OnyIcCYi5Vh9z5eh'
twitter_api_secret = 'kp3te4SEt76Gzs4nEY3odG5gIOStmlLyH3944xw3uq9C7z7Ovi'
twitter_callback_url = 'http://localhost:5000/callback/twitter'  # Adjust this URL accordingly

facebook_app_id = 'your_facebook_app_id'
facebook_app_secret = 'your_facebook_app_secret'
facebook_redirect_uri = 'http://localhost:5000/callback/facebook'

reddit_client_id = 'your_reddit_client_id'
reddit_client_secret = 'your_reddit_client_secret'
reddit_redirect_uri = 'http://localhost:5000/callback/reddit'

instagram_client_id = 'your_instagram_client_id'
instagram_client_secret = 'your_instagram_client_secret'
instagram_redirect_uri = 'http://localhost:5000/callback/instagram'

def get_access_token(request_token, verifier_pin):
    twitter = OAuth1Session(twitter_api_key, client_secret=twitter_api_secret,
                            resource_owner_key=request_token['oauth_token'],
                            resource_owner_secret=request_token['oauth_token_secret'])
    access_token = twitter.fetch_access_token('https://api.twitter.com/oauth/access_token',
                                              verifier=verifier_pin)
    return access_token


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    else:
        return redirect('/login')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Example validation - you should add proper validation and hashing of passwords
    if username in users:
        return render_template('register.html', error='Username already exists')
    else:
        users[username] = password
        return redirect('/login')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect('/dashboard')
        else:
            return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user_id'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session['user_id'])
    else:
        return redirect('/login')

@app.route('/connect/twitter')
def connect_twitter():
  twitter = OAuth1Session(twitter_api_key, client_secret=twitter_api_secret, callback_uri='oob')
  request_token = twitter.fetch_request_token('https://api.twitter.com/oauth/request_token')
  session['twitter_token'] = request_token
  auth_url = twitter.authorization_url('https://api.twitter.com/oauth/authorize')
  return redirect(auth_url)

@app.route('/complete/twitter', methods=['GET', 'POST'])
def complete_twitter():
    pin = request.form['pin']  # Assuming the PIN is submitted via a form
    access_token = get_access_token(session['twitter_token'], pin)
    print(access_token)
    session['twitter_access_token'] = access_token
    return redirect('/dashboard')



@app.route('/connect/facebook')
def connect_facebook():
    return redirect("https://www.facebook.com/v12.0/dialog/oauth?client_id=" + facebook_app_id + "&redirect_uri=" + facebook_redirect_uri + "&scope=public_profile,email")

@app.route('/connect/reddit')
def connect_reddit():
    reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, redirect_uri=reddit_redirect_uri, user_agent='web:flask_social_dashboard:v1.0.0')
    return redirect(reddit.auth.url(['identity'], '...', 'permanent'))

@app.route('/connect/instagram')
def connect_instagram():
    api = InstagramAPI(client_id=instagram_client_id, client_secret=instagram_client_secret, redirect_uri=instagram_redirect_uri)
    auth_url = api.get_authorize_url(scope=["basic"])
    return redirect(auth_url)

@app.route('/callback/twitter')
def twitter_callback():
  oauth_token = request.args.get('oauth_token')
  oauth_verifier = request.args.get('oauth_verifier')
  twitter = OAuth1Session(twitter_api_key, client_secret=twitter_api_secret, resource_owner_key=session['twitter_token']['oauth_token'], resource_owner_secret=session['twitter_token']['oauth_token_secret'])
  access_token = twitter.fetch_access_token('https://api.twitter.com/oauth/access_token', verifier=oauth_verifier)
  session['twitter_token'] = access_token
  return redirect('/dashboard')

@app.route('/callback/facebook')
def facebook_callback():
  # Retrieve authorization code from Facebook
  code = request.args.get('code')

  # Import Facebook library (assuming it's installed)
  from facebook import GraphAPI

  # Exchange code for access token using Facebook Graph API
  client = GraphAPI()
  access_token = client.exchange_code_for_access_token(
      client_id=facebook_app_id,
      client_secret=facebook_app_secret,
      code=code,
      redirect_uri=facebook_redirect_uri
  )

  # Store access token securely (consider database in production)
  session['facebook_token'] = access_token

  return redirect('/dashboard')

@app.route('/callback/reddit')
def reddit_callback():
  # Retrieve authorization code from Reddit
  code = request.args.get('code')

  # Exchange code for access token using Reddit's API
  reddit = praw.Reddit(client_id=reddit_client_id,
                       client_secret=reddit_client_secret,
                       redirect_uri=reddit_redirect_uri,
                       user_agent='web:flask_social_dashboard:v1.0.0')
  access_token = reddit.auth.authorize(code)

  # Store access token securely (consider database in production)
  session['reddit_token'] = access_token

  return redirect('/dashboard')

@app.route('/callback/instagram')
def instagram_callback():
  # Retrieve authorization code from Instagram
  code = request.args.get('code')

  # Import instagram.client library (assuming it's installed)
  import instagram

  # Exchange code for access token using Instagram's API
  client = instagram.client.InstagramAPI(client_id=instagram_client_id,
                                         client_secret=instagram_client_secret,
                                         redirect_uri=instagram_redirect_uri)
  access_token = client.exchange_code_for_access_token(code)

  # Store access token securely (consider database in production)
  session['instagram_token'] = access_token

  return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
