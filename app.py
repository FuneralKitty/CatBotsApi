from src.config import DB_CONFIG
from src.data_fullfilling import cat_colors_create_data, fullfill_cat_options
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import psycopg

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["600 per minute"]
)

valid_attributes = ['name', 'color', 'tail_length', 'whiskers_length']


@app.route('/ping', methods=['GET'])
def ping():
    return "Cats Service. Version 0.1", 200


@app.route('/cats', methods=['GET'])
@limiter.limit("600 per minute")
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


def validate_attributes(data):
    errors = []
    if 'name' not in data or not isinstance(data['name'], str):
        errors.append('Name is invalid')
    if 'color' not in data or not isinstance(data['color'], str):
        errors.append('Color is invalid')
    if 'tail_length' not in data or not isinstance(data['tail_length'], (int, float)) or data['tail_length'] <= 0:
        errors.append('Tail_length is invalid')
    if 'whiskers_length' not in data or not isinstance(data['whiskers_length'], (int, float)) or data[
        'whiskers_length'] <= 0:
        errors.append('Whiskers_length is invalid')

    if errors:
        return jsonify({'error': ' '.join(errors)}), 400

    return None


@app.route('/cat', methods=['POST'])
def add_info():
    data = request.get_json()

    validation_response = validate_attributes(data)
    if validation_response:
        return validation_response

    try:
        conn = psycopg.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM cats WHERE name = %s", (data['name'],))
            existing_cat = cur.fetchone()

            if existing_cat:
                return jsonify({'error': 'Cat already exists'}), 409

            cur.execute("""
                INSERT INTO cats (name, color, tail_length, whiskers_length)
                VALUES (%s, %s, %s, %s)
            """, (data['name'], data['color'], data['tail_length'], data['whiskers_length']))
            conn.commit()

            return jsonify({'message': 'Cat added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    cat_colors_create_data(DB_CONFIG)
    fullfill_cat_options(DB_CONFIG)