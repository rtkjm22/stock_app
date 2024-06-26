from flask import Blueprint, jsonify, request
from . import db
from .models import User

main_bp = Blueprint('main', __name__, url_prefix='/')
users_bp = Blueprint('users', __name__, url_prefix='/users')
companies_bp = Blueprint('companies', __name__, url_prefix='/companies')

@users_bp.route('/', methods=['GET'])
def user_list():
  users = db.session.execute(db.select(User).order_by(User.name)).scalars().all()
  return jsonify([user.to_dict() for user in users]), 200

@users_bp.route('/create', methods=["POST"])
def user_create():
  data = request.form
  user = User(
    name=data["name"],
    email=data["email"]
  )
  db.session.add(user)
  db.session.commit()
  return jsonify(user.to_dict()), 201


def init_app(app):
  app.register_blueprint(main_bp)
  users_bp.register_blueprint(companies_bp)
  app.register_blueprint(users_bp)