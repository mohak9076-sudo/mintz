from app import app
from models import db, User, Expense, HangoutSplit
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Create demo user
    demo_user = User(
        name="Alex Rivers",
        email="student@college.edu",
        password=generate_password_hash("password123"),
        onboarding_complete=True,
        goal_name="MacBook Pro M-Series",
        goal_amount=1500.0,
        monthly_allowance=800.0,
        save_percentage=25.0,
        target_savings=200.0,
        current_spent=284.50,
        risk_profile="Balanced",
        health_score=82
    )
    db.session.add(demo_user)
    db.session.commit()
    
    # Add initial dummy expenses
    e1 = Expense(user_id=demo_user.id, title="Midnight Taco Bell Run", amount=18.50, category="Dining Out", ai_verdict="Impulse Trap 🚨", status="Bad")
    e2 = Expense(user_id=demo_user.id, title="Python & Cloud Textbook", amount=62.00, category="Education", ai_verdict="Major W Investment 🧠", status="Good")
    e3 = Expense(user_id=demo_user.id, title="Trader Joe's Essentials", amount=54.00, category="Groceries", ai_verdict="Chef Moves ✨", status="Good")
    
    # Add initial hangout split
    s1 = HangoutSplit(user_id=demo_user.id, title="Roadtrip Gas & Snacks", total=120.0, paid_by="You", friends="Sam, Maya, Leo", your_share=30.0, owed_to_you=90.0, status="Unsettled")
    
    db.session.add_all([e1, e2, e3, s1])
    db.session.commit()
    
    print("✨ Database vibe_finance.db initialized with demo data!")