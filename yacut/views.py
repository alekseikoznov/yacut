from random import choice
from string import ascii_letters, digits
from flask import abort, flash, redirect, render_template
from re import match
from . import app, db
from .forms import LinkForm
from .models import URLMap


def get_unique_short_id():
    letters = ascii_letters + digits
    while True:
        random_link = ''.join(choice(letters) for i in range(6))
        if URLMap.query.filter_by(short=random_link).first() is None:
            break
    return random_link


def correct_short(short):
    pattern = "^[A-Za-z0-9]*$"
    return bool(match(pattern, short))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        print(type(form.custom_id.data))
        if short:
            if URLMap.query.filter_by(short=short).first():
                flash(f'Имя {short} уже занято!')
                return render_template('main.html', form=form)
            elif not correct_short(short):
                flash('Указано недопустимое имя для короткой ссылки')
                return render_template('main.html', form=form)
        else:
            short = get_unique_short_id()
        link = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(link)
        db.session.commit()
        return render_template('main.html', form=form, link=link)
    return render_template('main.html', form=form)


@app.route('/<path:link>')
def redirect_view(link):
    link = URLMap.query.filter_by(short=link).first()
    if link:
        return redirect(link.original)
    abort(404)