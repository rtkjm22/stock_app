from .controllers.main_controller import main_bp
from .controllers.user_controller import users_bp
from .controllers.stock_controller import stocks_bp

def init_app(app):
  app.register_blueprint(main_bp)
  app.register_blueprint(users_bp)
  app.register_blueprint(stocks_bp)