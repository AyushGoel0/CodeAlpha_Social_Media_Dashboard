from flask import Flask, render_template, redirect, request, session
import praw

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Dummy user database
users = {
    'user': 'password'  # Store hashed passwords in production
}

# Social media API credentials
reddit_client_id = 'Y38c9NasW3anMdXwIcCeiA'
reddit_client_secret = 'lycMolGxPNP1bRpdar_c7YucaKeetw'
reddit_redirect_uri = 'http://localhost:5000/callback/reddit'

def fetch_reddit_feeds():
    # Function to fetch Reddit feeds using the PRAW library
    # Example implementation assuming you have installed the `praw` package
    import praw

    # Initialize Reddit instance with access token
    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         redirect_uri=reddit_redirect_uri,
                         user_agent='web:flask_social_dashboard:v1.0.0')

    # Fetch submissions from a subreddit
    submissions = reddit.subreddit('all').hot(limit=10)  # Fetching top 10 hot submissions

    # Extract submission titles
    reddit_feeds = [submission.title for submission in submissions]

    return reddit_feeds

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
        # Fetch feeds data from Reddit
        reddit_data = fetch_reddit_feeds()      # Replace with your function to fetch Reddit feeds

        return render_template('dashboard.html', username=session['user_id'],
                               reddit_data=reddit_data)
    else:
        return redirect('/login')

@app.route('/connect/reddit')
def connect_reddit():
    reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, redirect_uri=reddit_redirect_uri, user_agent='web:flask_social_dashboard:v1.0.0')
    return redirect(reddit.auth.url(scopes=['identity'], state='...', duration='permanent'))

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

if __name__ == '__main__':
    app.run(debug=True)
