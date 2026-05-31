from flask import Flask, render_template, send_from_directory, abort
from flask_flatpages import FlatPages
from datetime import datetime
import os, json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['FLATPAGES_ROOT'] = 'content'
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['tables', 'fenced_code', 'codehilite']
pages = FlatPages(app)


def get_posts():
    posts = [p for p in pages if p.meta.get('date')]
    posts.sort(key=lambda p: p.meta['date'], reverse=True)
    return posts


def load_quiz_json(quiz_id):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    # Map quiz IDs to filenames
    quiz_map = {
        '001': 'quiz_001.json',
    }
    filename = quiz_map.get(quiz_id)
    if not filename:
        return None
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    return render_template('hub.html', posts=get_posts())


@app.route('/practice/<quiz_id>/')
def practice(quiz_id):
    quiz = load_quiz_json(quiz_id)
    if not quiz:
        abort(404)
    # Compute objective and subjective totals
    obj = sum(len(s['questions']) for s in quiz['sections'] if s['type'] in ('choice', 'fill'))
    subj = sum(len(s['questions']) for s in quiz['sections'] if s['type'] in ('short', 'write'))
    quiz['objective_total'] = obj
    quiz['subjective_total'] = subj
    return render_template('quiz.html', quiz=quiz)


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
