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
from pydantic import BaseModel, field_validator, ValidationError


app_name = "Cats Service"
app = Flask(__name__)
limiter = Limiter(
    app=app, key_func=get_remote_address, default_limits=["600 per minute"]
)

class Cat(BaseModel):
    name: str
    color: str
    tail_length: int
    whiskers_length: int

    @classmethod
    @field_validator('tail_length')
    def check_tail_length(cls, value):
        if value <= 0:
            raise ValueError("Tail length must be greater than zero")
        return value

    @classmethod
    @field_validator('whiskers_length')
    def check_whiskers_length(cls, value):
        if value <= 0:
            raise ValueError("Whiskers length must be greater than zero")
        return value

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


@app.route("/cat", methods=["POST"])
def add_info() -> tuple[dict[str, str], int] | tuple[Response, int]:
    try:
        data_cats = Cat(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    result: Tuple[Dict[str, Any], int] = add_info_db(data_cats.dict())
    return jsonify(result[0]), result[1]


if __name__ == "__main__":
    cat_colors_create_data(DB_CONFIG)
    fullfill_cat_options(DB_CONFIG)
