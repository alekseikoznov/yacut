from flask import jsonify, request

from . import app, db
from .models import URLMap
from .views import get_unique_short_id, correct_short
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    elif 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if data.get('custom_id'):
        if len(data['custom_id']) > 16 or not correct_short(data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        elif URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    else:
        data['custom_id'] = get_unique_short_id()
    print(data)
    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_opinion(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200