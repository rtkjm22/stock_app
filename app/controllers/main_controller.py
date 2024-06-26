from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    return jsonify({"main_bp": "呼び出されました。"})
