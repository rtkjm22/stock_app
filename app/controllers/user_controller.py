from flask import Blueprint, jsonify, request
from .. import db
from ..models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/users')

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
