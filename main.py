from flask import Flask, request, jsonify
import psycopg
from src.config import DB_CONFIG
from src.First_quest import first_quest
from src.second_quest import second_quest

app = Flask(__name__)

valid_attributes = ['name', 'color', 'tail_length', 'whiskers_length']


@app.route('/ping', methods=['GET'])
def ping():
    return "Cats Service. Version 0.1", 200


@app.route('/cats', methods=['GET'])
def data_parser():
    attribute = request.args.get("attribute", default='name')
    order = request.args.get("order", default='asc')
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=10, type=int)

    if attribute not in valid_attributes:
        return jsonify({'error': 'Invalid attribute'}), 400
    if order not in ['asc', 'desc']:
        return jsonify({'error': 'Invalid order'}), 400

    db_request = f"""
                SELECT name, color, tail_length, whiskers_length
                FROM cats
                ORDER BY {attribute} {order}
                OFFSET %s LIMIT %s
                """
    try:
        conn = psycopg.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(db_request, (offset, limit))
            cats = cur.fetchall()
            if not cats:
                return jsonify({'error': 'No cats found'}), 404

            data = [
                {'name': cat[0], 'color': cat[1], 'tail_length': cat[2], 'whiskers_length': cat[3]}
                for cat in cats
            ]
            return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    first_quest(DB_CONFIG)
    second_quest(DB_CONFIG)
    app.run(host='0.0.0.0', port=8080)
