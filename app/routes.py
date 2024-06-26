from flask import Blueprint, jsonify
from .controllers.main_controller import main_bp
from .controllers.user_controller import users_bp
from .controllers.stock_controller import stocks_bp
import yfinance as yf
import pprint
import pandas as pd

def init_app(app):
  app.register_blueprint(main_bp)
  app.register_blueprint(users_bp)
  app.register_blueprint(stocks_bp)