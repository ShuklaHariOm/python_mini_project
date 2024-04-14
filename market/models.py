from market import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=50), nullable=False, unique=True)
    email_add = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'User {self.username}'

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'₹{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'₹{self.budget}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password)

    def check_password_correction(self, attempted_password):
        return check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    __tablename__ = 'item'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner=None
        user.budget += self.price
        db.session.commit()


class stocks(db.Model):
    __tablename__ = 'stocks'
    __table_args__ = {'extend_existing': True}
    stock_id = db.Column(db.Integer(), primary_key=True)
    stock_name = db.Column(db.String(length=30))
    stock_value = db.Column(db.String(length=10))
    variation = db.Column(db.Integer())
    percent_change = db.Column(db.String(length=10))
    date_time = db.Column(db.String(length=20))

    def __repr__(self):
        return f'Stock {self.stock_name}'


class company(db.Model):
    __tablename__ = 'company'
    __table_args__ = {'extend_existing': True}
    symbol = db.Column(db.String(length=11), primary_key=True)
    company_name = db.Column(db.String(length=30))

    def __repr__(self):
        return f'Company {self.symbol}'


with app.app_context():
    db.create_all()
