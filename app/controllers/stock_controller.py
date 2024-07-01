from flask import Blueprint, jsonify
from ..services.stock_service import get_stock_list, get_filtered_stock_list

stocks_bp = Blueprint('stocks', __name__, url_prefix='/stocks')

@stocks_bp.route('/', methods=["GET"])
def get_stocks():
  target = 'tiker_jpx.csv'
  get_stock_list(target)
  return jsonify({'stocks': '打たれました。'}), 200

@stocks_bp.route('/list', methods=["GET"])
def get_filtered():
  get_filtered_stock_list('data_jpx.csv')
  return jsonify({'stocks': 'list'}), 200