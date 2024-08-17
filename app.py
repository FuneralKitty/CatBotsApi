from typing import Any, Tuple, Dict
from src.config import DB_CONFIG
from src.data_fullfilling import (
    cat_colors_create_data,
    fullfill_cat_options,
    add_info_db,
    get_parsed_data,
)
from flask import Flask, request, jsonify, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address




app_name = "Cats Service"
app = Flask(__name__)
limiter = Limiter(
    app=app, key_func=get_remote_address, default_limits=["600 per minute"]
)


@app.route("/ping", methods=["GET"])
def ping() -> Tuple[str, int]:
    return f"{app_name}. Version 0.1", 200


@app.route("/cats", methods=["GET"])
@limiter.limit("600 per minute")
def data_parser() -> tuple[Response, int]:
    attribute = request.args.get("attribute", default="name")
    order = request.args.get("order", default="asc")
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=10, type=int)

    result: Tuple[Dict[str, str], int] = get_parsed_data(attribute, order, offset, limit)
    return jsonify(result[0]), result[1]


def validate_attributes(data) -> tuple[Response, int] | None:
    # FIXMI: возможно сделать через pydantic
    errors = []
    if "name" not in data or not isinstance(data["name"], str):
        errors.append("Name is invalid")
    if "color" not in data or not isinstance(data["color"], str):
        errors.append("Color is invalid")
    if (
        "tail_length" not in data
        or not isinstance(data["tail_length"], (int, float))
        or data["tail_length"] <= 0
    ):
        errors.append("Tail_length is invalid")
    if (
        "whiskers_length" not in data
        or not isinstance(data["whiskers_length"], (int, float))
        or data["whiskers_length"] <= 0
    ):
        errors.append("Whiskers_length is invalid")

    if errors:
        return jsonify({"error": " ".join(errors)}), 400

    return None


@app.route("/cat", methods=["POST"])
def add_info() -> tuple[dict[str, str], int] | tuple[Response, int]:
    data = request.get_json()
    validation_response = validate_attributes(data)
    if validation_response:
        return validation_response

    result: Tuple[Dict[str, Any], int] = add_info_db(data)
    return jsonify(result[0]), result[1]


if __name__ == "__main__":
    cat_colors_create_data(DB_CONFIG)
    fullfill_cat_options(DB_CONFIG)
