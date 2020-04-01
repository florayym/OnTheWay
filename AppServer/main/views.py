from flask import request, jsonify, url_for
from . import main
from .. import db
from ..models import User, Comment
import datetime
import csv
from .utils import *
from flask_login import login_user, logout_user, login_required, current_user

from itsdangerous import URLSafeTimedSerializer, SignatureExpired
s = URLSafeTimedSerializer('Thisisasecret!')
MAX_AGE = 3600

def create_stroe():
    print('i am here')
    with open('./tmp/store1.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                store = Store(storename=row[0],
                              location=row[1],
                              longtitude=row[2],
                              latitude=row[3],
                              score=0 if len(row[4]) == 0 else row[4],
                              special=row[5],
                              img_url=row[6],
                              )
                db.session.add(store)
        db.session.commit()
    print('*' * 20, '商铺信息录入完成', '*' * 20)


def create_comment():
    id = 0
    former = ''
    with open('./tmp/comment1.csv') as f:
        reader = csv.reader(f)
        user = User.query.first()
        for row in reader:
            if len(row) > 0:
                if row[0] != former:
                    id += 1
                    former = row[0]
                StoreNO = id
                store = Store.query.get(StoreNO)
                str_time = row[3].strip().split('-')
                time = datetime.date(int(str_time[0]), int(str_time[1]), int(str_time[2]))
                comment = Comment(poster=user, store=store,
                                  comment=row[1],
                                  comment_time=time,
                                  comment_score=row[2])
                db.session.add(comment)
        db.session.commit()
    print('*' * 20, '评论信息录入完成', '*' * 20)


@main.route('/message', methods=['POST', 'GET'])
def message():
    return jsonify({
        'message': 'please login!'
    })


@main.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(password):
        login_user(user)
        return jsonify({
            'message': 'login success',
        })
    else:
        return jsonify({
            'message': 'login failure',
        })


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        'message': 'logout success',
    })


@main.route('/register', methods=['POST', 'GET'])
def register():
    username = request.form['username']
    email = request.form['email']
    if User.query.filter_by(username=username).first():
        return jsonify({
            'message': 'username exist'
        })
    if User.query.filter_by(email=email).first():
        return jsonify({
            'message': 'email exist'
        })

    user = User(username=username,
                password=request.form['password'],
                email=email,
                tel=request.form['tel'],
                sex=request.form['sex'],
                birth=birth(request.form['birth']),
                tags=request.form['tags'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'register success',
    })


# 推荐系统
@main.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    recommended = recommend(latitude, longitude)
    return jsonify({
        'messages': 'success',
        'recommend list': recommended
    })


@main.route('/search', methods=['POST'])
# @login_required
def search():
    storename = request.form['storename'].strip()
    stores = Store.query.filter(Store.storename.like('%{}%'.format(storename))).all()
    if len(stores) != 0:
        details = list()
        for store in stores:
            details.append({
                'store_id': store.id,
                'img_url': store.img_url,
                'store': store.storename,
                'score': store.score,
                'distance': calDistance(request.form['latitude'], request.form['longitude'],
                                        store.latitude, store.longtitude)
            })
        return jsonify({
            'messages': 'success',
            'search result': details,
        })
    else:
        return jsonify({
            'message': 'store not exists',
            'search result': None,
        })


@main.route('/details', methods=['POST', 'GET'])
# @login_required
def details():
    store = Store.query.get(request.form['store_id'])
    user = current_user._get_current_object()
    word_cloud = url_for('static', _external=True, filename='images/word_cloud/stores/{}.png'.format(store.id))
    return jsonify({
        'username': user.username,
        'img_url': store.img_url,
        'score': store.score,
        'word_cloud': word_cloud,
    })


@main.route('/comments', methods=['POST', 'GET'])
# @login_required
def comment():
    store = Store.query.get(request.form['store_id'])
    comments = Comment.query.filter_by(store_id=store.id).paginate(int(request.form['page']),
                                                                   int(request.form['per_page']), False)
    comment_list = list()
    if len(comments.items) == 0:
        return jsonify({
            'page': request.form['page'],
            'comments': None,
            'message': 'out of the maximum',
        })
    for comment in comments.items:
        comment_list.append({
            'user': comment.poster.username,
            'comment_score': comment.comment_score,
            'comment_time': comment.comment_time,
            'comment': comment.comment
        })
    return jsonify({
        'page': request.form['page'],
        'comments': comment_list,
        'message': 'success',
    })


@main.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    score = request.form['score']
    store = Store.query.get(request.form['store_id'])
    comment = Comment(comment=request.form['comment'],
                      comment_score=mark(request.form['comment']),
                      poster=current_user._get_current_object(),
                      store=store,
                      )
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        'message': 'upload success',
    })


@main.route('/create_database', methods=['POST', 'GET'])
def create_database():
    db.create_all()
    user = User(username='admin',
                password='admin',
                email='Liuxm@mail.hfut.edu.cn')
    db.session.add(user)
    db.session.commit()
    create_stroe()
    create_comment()
    return 'success'

@main.route('/update_word_cloud', methods=['POST', 'GET'])
# @login_required
def update_word_cloud():
    store = Store.query.get(request.form['store_id'])
    try:
        generate_word_cloud(store)
    except Exception as e:
        return jsonify({
            'message': 'failure',
            'word_cloud': None,
        })
    return jsonify({
        'message': 'success',
        'word_cloud': url_for('static', _external=True, filename='images/word_cloud/stores/{}.png'.format(store.id)),
    })


@main.route('/request_verification', methods=['GET', 'POST'])
def request_verification():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

    username = request.form['username']
    email = request.form['email']

    token = s.dumps(email, salt='email-confirm')
    msg = Message('Confirm Email', sender='yuyim@126.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = '<h1>Dear {},<br><br>your email verification link is {}. It will be expired within {} minutes.</h1>'.format(username, link, (int) MAX_AGE/60)

    mail.send(msg)

    return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)


@main.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=MAX_AGE)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>Email address erified!</h1>'


@main.route('/test', methods=['GET', 'POST'])
def test():
    return '服务器运行正常'















