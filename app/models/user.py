from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .. import db

class User(Base):
  __tablename__ = 'user'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(unique=True)
  email: Mapped[str]

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email
    }
