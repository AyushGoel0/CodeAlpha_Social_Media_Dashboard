# CodeAlpha_Social_Media_Dashboard

# Flask Social Media Dashboard

This Flask application provides a social media dashboard where users can log in, register, and view their social media feeds, particularly from Reddit. It also allows users to connect their Reddit account to fetch Reddit feeds.

## Folder Structure:

tree CodeAlpha_Social_Media_Dashboard/
├── myenv
├── app.py
├── static
│   └── style.css
├── templates
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── README.md
└── requirements.txt

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/flask-social-media-dashboard.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Log in with your username and password, or register for a new account.
3. Once logged in, you will be redirected to the dashboard where you can view your social media feeds.
4. If you haven't connected your Reddit account yet, you can do so by clicking on "Connect with Reddit".
5. Enjoy viewing your Reddit feeds on the dashboard!

## Files

- **app.py**: Main Flask application file containing the routes and logic.
- **templates/**: Directory containing HTML templates for the login, registration, and dashboard pages.
- **login.html**: HTML template for the login page.
- **register.html**: HTML template for the registration page.
- **dashboard.html**: HTML template for the dashboard page.
- **static/style.css**: CSS file containing styles for the application.


## Dependencies

- Flask: Web framework for Python.
- praw: Python Reddit API Wrapper for accessing Reddit's API.
- Other dependencies specified in `requirements.txt`.

## Configuration

- `app.secret_key`: Secret key used for session management. Replace `'your_secret_key'` with a secure random string.
- Reddit API credentials (`reddit_client_id`, `reddit_client_secret`, `reddit_redirect_uri`): Replace with your own credentials obtained from Reddit's API dashboard.

## Authors

- [Your Name](https://github.com/yourusername)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
