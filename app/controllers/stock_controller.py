from flask import Blueprint, jsonify
from ..services.stock_service import stock_list

stocks_bp = Blueprint('stocks', __name__, url_prefix='/stocks')

@stocks_bp.route('/', methods=["GET"])
def stocks():
  target = 'sample.csv'
  stock_list(target)
  return jsonify({'stocks': '打たれました。'}), 200