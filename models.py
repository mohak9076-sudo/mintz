from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    onboarding_complete = db.Column(db.Boolean, default=False)
    
    # Financial Profile & Editable Goals
    goal_name = db.Column(db.String(150), default="Emergency Bag")
    goal_amount = db.Column(db.Float, default=10000.0)
    monthly_allowance = db.Column(db.Float, default=5000.0)
    save_percentage = db.Column(db.Float, default=20.0)
    target_savings = db.Column(db.Float, default=1000.0)
    current_spent = db.Column(db.Float, default=0.0)
    risk_profile = db.Column(db.String(50), default="Balanced")
    health_score = db.Column(db.Integer, default=80)
    
    # Gamification, Streaks & Cyber Pet
    streak_count = db.Column(db.Integer, default=1)
    pet_type = db.Column(db.String(50), default="cat")   # 'cat', 'dog', 'robot'
    pet_name = db.Column(db.String(100), default="Byte")
    last_active_date = db.Column(db.String(20), default=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relational Associations
    expenses = db.relationship("Expense", backref="user", lazy=True, cascade="all, delete-orphan")
    friends = db.relationship("Friend", backref="user", lazy=True, cascade="all, delete-orphan")
    splits = db.relationship("HangoutSplit", backref="user", lazy=True, cascade="all, delete-orphan")
    subscriptions = db.relationship("Subscription", backref="user", lazy=True, cascade="all, delete-orphan")

class Friend(db.Model):
    __tablename__ = "friends"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    upi_id = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    ai_verdict = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), default=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HangoutSplit(db.Model):
    __tablename__ = "hangout_splits"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    total = db.Column(db.Float, nullable=False)
    paid_by = db.Column(db.String(100), default="You")
    friends_list = db.Column(db.Text, nullable=False)
    your_share = db.Column(db.Float, nullable=False)
    owed_to_you = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Unsettled")
    date = db.Column(db.String(20), default=lambda: datetime.utcnow().strftime("%b %d"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Subscription(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(db.String(50), default="Monthly")
    category = db.Column(db.String(80), nullable=False)
    renewal_day = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="Bad")
    ai_verdict = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)