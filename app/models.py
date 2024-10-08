import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Client(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    login: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    task: so.Mapped[list["task"]] = so.Relationship()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Client {self.login}>'

class task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    creator: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Client.id))

    def __repr__(self):
        return f'<Task {self.name}>'


@login.user_loader
def load_user(id):
    return db.session.get(Client, int(id))