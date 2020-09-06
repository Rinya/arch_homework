import json
import os

from flask import Flask, request, jsonify
from sqlalchemy import create_engine

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME']
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']

engine = create_engine(config['DATABASE_URI'], echo=True)


@app.route("/health")
def health():
    return '{"status": "ok"}'


@app.route("/version")
def version():
    return '{"version": "1.0"}'


@app.route('/db')
def db():
    with engine.connect() as connection:
        result = connection.execute("select id, username from client;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)


@app.route("/config")
def configuration():
    return json.dumps(config)


@app.route("/users", methods=["GET"])
def get_all_users():
    try:
        with engine.connect() as connection:
            result = connection.execute("select id, username from client;")
            rows = [dict(r.items()) for r in result]
        return json.dumps(rows)
    except Exception as e:
        print("get_user_list. exception: %s" % e)


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        with engine.connect() as connection:
            sql = "select id, username from client where id=%s;" % user_id
            app.logger.info('sql: %s', sql)
            result = connection.execute(sql)
            rows = [dict(r.items()) for r in result]
        return json.dumps(rows)
    except Exception as e:
        print("get_user_list. exception: %s" % e)


@app.route("/user", methods=["POST"])
def add_user():
    connection = engine.connect()
    trans = connection.begin()

    try:
        req = request.get_json()
        _name = req['name']
        app.logger.info('_name: %s', _name)
        if _name and request.method == 'POST':
            sql = "insert into client(username) values('%s');" % _name
            app.logger.info('sql: %s', sql)
            connection.execute(sql)
            trans.commit()
        return "User %s was added" % _name
    except Exception as e:
        print("add_user. exception: %s" % e)
        trans.rollback()


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        req = request.get_json()
        _name = req['name']
        if user_id and _name and request.method == 'PUT':
            with engine.connect() as connection:
                sql = "update client set username = '%s' where id = %s;" % (_name, user_id)
                app.logger.info('sql: %s', sql)
                connection.execute(sql)
        return "User with id %s was updated" % user_id
    except Exception as e:
        print("update_user. exception: %s" % e)


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        if request.method == 'DELETE':
            with engine.connect() as connection:
                sql = "delete from client where id = %s;" % user_id
                app.logger.info('sql: %s', sql)
                connection.execute(sql)
        return "User with id %s was deleted" % user_id
    except Exception as e:
        print("update_user. exception: %s" % e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)