from flask import Flask, render_template, request, redirect, url_for
from models import db, URL
import random, string
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db.init_app(app)

def generate_short_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme and parsed.netloc

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('url')

        if not is_valid_url(original_url):
            return render_template('home.html', error="Invalid URL")

        short_code = generate_short_code()
        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + short_code

    return render_template('home.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if url:
        return redirect(url.original_url)

    return "URL not found", 404


@app.route('/history')
def history():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template('history.html', urls=urls)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
