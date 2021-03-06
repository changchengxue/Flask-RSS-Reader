import feedparser

from . import app
from . import db
from . import lm
from .forms import LoginForm
from .forms import MarkForm
from .forms import UserRegisterForm
from .forms import UserProfileForm
from .models import Mark
from .models import User

from flask import g
from flask import abort
from flask import flash
from flask import session
from flask import url_for
from flask import request
from flask import jsonify
from flask import redirect
from flask import current_app
from flask import render_template

from datetime import datetime
from bs4 import BeautifulSoup as BSoup

from urllib.request import urlopen
from urllib.parse import urlparse, urljoin

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from cryptacular.bcrypt import BCRYPTPasswordManager as bMan


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(401)
def unauthorized(error):
    flash('Unauthorized access', category='error')
    return redirect(url_for('login'))


@app.errorhandler(403)
def forbidden(error):
    flash('Forbidden access', category='error')
    return redirect(url_for('marks'))


@app.route('/')
@app.route('/index')
@app.route('/marks')
@app.route('/marks/<int:page>')
@login_required
def marks(page=1):
    u = g.user
    return render_template('mark/index.html',
                           title='Marks - page {}'.format(page),
                           header='',
                           marks=u.marks(page),
                           suggestions=u.suggestions(),
                           recently=u.recent())


@app.route('/mark/new', methods=['GET', 'POST'])
@login_required
def new_mark():
    form = MarkForm()
    if form.validate_on_submit():
        if g.user.murl(form.url.data):
            flash('Mark with this url ({}) already\
                  exists'.format(form.url.data), category='error')
            return redirect(url_for('marks'))
        m = Mark()
        form.populate_obj(m)
        m.owner_id = g.user.id
        m.created = datetime.utcnow()
        if form.tags.data:
            m.tags = ' '.join([t.strip()
                              for t in form.tags.data.strip().split(',')])\
                        .lower()
        m.clicks = 0
        if not form.title.data:
            soup = BSoup(urlopen(form.url.data), 'html.parser')
            m.title = soup.title.string
        db.session.add(m)
        db.session.commit()
        flash('New mark {} added'.format(m.title), category='info')
        return redirect(url_for('marks'))
    if request.args.get('url'):
        form.url.data = request.args.get('url')
    if request.args.get('title'):
        form.title.data = request.args.get('title')
    if request.args.get('type') == 'feed':
        form.type.data = 'feed'
    return render_template('mark/new.html',
                           title='New mark',
                           form=form)


@app.route('/mark/view/<int:id>', methods=['GET'])
@login_required
def view_mark(id):
    m = g.user.mid(id)
    if not m:
        abort(403)
    if m.type != 'feed':
        abort(404)
    data = feedparser.parse(m.url)
    if m:
        if not m.clicks:
            m.clicks = 0
        m.last_clicked = datetime.utcnow()
        m.clicks += 1
        db.session.add(m)
        db.session.commit()
    return render_template('mark/view.html',
                           mark=m,
                           data=data,
                           title=m.title,
                           )


@app.route('/mark/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mark(id):
    m = g.user.mid(id)
    form = MarkForm(obj=m)
    if not m:
        abort(403)
    if form.validate_on_submit():
        if m.url != form.url.data and g.user.murl(form.url.data):
            flash('Mark with this url ({}) already\
                  exists'.format(form.url.data), category='error')
            return redirect(url_for('marks'))
        form.populate_obj(m)
        m.updated = datetime.utcnow()
        db.session.add(m)
        db.session.commit()
        flash('Mark {} updated'.format(form.title.data), category='info')
        if form.referrer.data and is_safe_url(form.referrer.data):
            return redirect(form.referrer.data)
        return redirect(url_for('marks'))
    form.referrer.data = request.referrer
    return render_template('mark/edit.html',
                           title='Edit mark - {}'.format(m.title),
                           form=form)


@app.route('/mark/delete/<int:id>')
@login_required
def delete_mark(id):
    m = g.user.mid(id)
    if m:
        db.session.delete(m)
        db.session.commit()
        flash('Mark {} deleted'.format(m.title), category='info')
        return redirect(url_for('marks'))
    abort(403)


@app.route('/mark/tag/<slug>')
@app.route('/mark/tag/<slug>/<int:page>')
@login_required
def mark_q_tag(slug, page=1):
    m = g.user.tag(slug, page)
    return render_template('mark/index.html',
                           title='Mark results',
                           header='Mark results for ' + slug,
                           marks=m)


@app.route('/search', methods=['GET'])
@app.route('/search/<int:page>', methods=['GET'])
@login_required
def search_string(page=1):
    q = request.args.get('q')
    t = request.args.get('type')

    if not q and not t:
        return redirect(url_for('marks'))

    m = g.user.string(page, q, t)
    return render_template('mark/index.html',
                           title='Mark results',
                           header="Mark results for {} - {}".format(q, t),
                           marks=m)


@app.route('/mark/inc')
@login_required
def ajax_mark_inc():
    if request.args.get('id'):
        id = int(request.args.get('id'))
        m = g.user.mid(id)
        if m:
            if not m.clicks:
                m.clicks = 0
            m.last_clicked = datetime.utcnow()
            m.clicks += 1
            db.session.add(m)
            db.session.commit()
            return jsonify(status='success')
        return jsonify(status='forbidden')
    return jsonify(status='error')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    u = g.user
    mc = g.user.mark_count()
    bc = g.user.bookmark_count()
    fc = g.user.feed_count()
    lcm = g.user.mark_last_created()
    form = UserProfileForm(obj=u)
    if form.validate_on_submit():
        form.populate_obj(u)
        if form.password.data:
            pm = bMan()
            u.password = pm.encode(form.password.data)
        else:
            del u.password
        db.session.add(u)
        db.session.commit()
        flash('User {} updated'.format(form.username.data), category='info')
        return redirect(url_for('profile'))
    return render_template('account/profile.html',
                           form=form,
                           title='Profile',
                           mc=mc,
                           bc=bc,
                           fc=fc,
                           lcm=lcm,
                           )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not app.config['CAN_REGISTER']:
        abort(403)
    form = UserRegisterForm()
    if form.validate_on_submit():
        u = User()
        pm = bMan()
        form.populate_obj(u)
        u.password = pm.encode(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('New user {} registered'.format(form.username.data), category='info')
        return redirect(url_for('login'))
    return render_template('account/register.html',
                           form=form,
                           title='Register',
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated:
        return redirect(url_for('marks'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.by_uname_or_email(form.username.data)
        if u and u.authenticate_user(form.password.data):
            u.last_logged = datetime.utcnow()
            db.session.add(u)
            db.session.commit()
            flash('Successful login request for {}'.format(u.username),
                  category='info')
            login_user(u, remember=form.remember_me.data)
            return redirect(url_for('marks'))
        else:
            flash('Failed login request for {}'.format(form.username.data),
                  category='error')
            return redirect(url_for('login'))
    return render_template('account/login.html',
                           title='Login',
                           form=form,
                           )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/redirect/<int:id>')
@login_required
def mark_redirect(id):
    url = url_for('mark_meta', id=id)
    return render_template('meta.html', url=url)


@app.route('/meta/<int:id>')
@login_required
def mark_meta(id):
    b = g.user.bid(id)
    if b:
        return render_template('meta.html', url=b.url)
    abort(403)


# yanked from flask.pocoo.org/snippets/62
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and\
        ref_url.netloc == test_url.netloc
