from flask import flash, redirect, render_template
from . import app, db
from .forms import LinkForm
from .models import URLMap
from .utils import get_unique_short_id, correct_short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                flash(f'Имя {custom_id} уже занято!')
                return render_template('main.html', form=form)
            elif not correct_short(custom_id):
                flash('Указано недопустимое имя для короткой ссылки')
                return render_template('main.html', form=form)
        else:
            custom_id = get_unique_short_id()
        link = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(link)
        db.session.commit()
        return render_template('main.html', form=form, link=link)
    return render_template('main.html', form=form)


@app.route('/<path:link>')
def redirect_view(link):
    link = URLMap.query.filter_by(short=link).first_or_404()
    return redirect(link.original)