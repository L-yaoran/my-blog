from flask import Flask, render_template
from flask_flatpages import FlatPages
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-local-only')
app.config['FLATPAGES_ROOT'] = 'content'
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['tables', 'fenced_code', 'codehilite']
pages = FlatPages(app)


def get_posts():
    posts = [p for p in pages if p.meta.get('date')]
    posts.sort(key=lambda p: p.meta['date'], reverse=True)
    return posts


@app.route('/')
def index():
    return render_template('hub.html', posts=get_posts())


@app.route('/<path:slug>/')
def post(slug):
    post = pages.get_or_404(slug)
    return render_template('post.html', post=post)


@app.route('/hub')
def hub():
    return render_template('hub.html', posts=get_posts())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')


@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
