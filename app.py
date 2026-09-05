"""
========================================================================================
MINTZ: AI-POWERED GEN Z WEALTH OPERATING SYSTEM & REAL-TIME CASHFLOW INTELLIGENCE
========================================================================================
Core Application Backend Server & Actuarial Financial Computation Suite
Stack: Flask, SQLAlchemy ORM, SQLite / PostgreSQL, Jinja2, Chart.js, Google Gen AI SDK

Architectural Modules:
  1. Multi-Factor Deterministic Vibe Health Score Engine (100-Point Model)
  2. Actuarial Spending Velocity & Stochastic Monte Carlo Goal Forecast Simulator
  3. Comprehensive Indian Banking Multi-Pattern Regex SMS / UPI Tokenizer
  4. Reactive Cyber Tamagotchi Pet Companion State & Evolution Engine
  5. Multi-Cycle Recurring Auto-Subscription Overhead & Leak Audit Suite
  6. FinBro Persona Intelligence Agent (Roast / Hype / Guru) with Context Telemetry
  7. Social Hangout Ledger (Dudesy) with Peer Settlement Tracking
  8. Micro-SIP Annuity Due Future-Value Compounding Modeler (Stonks)
  9. Data Integrity, Error Handling & Cryptographic Session Security Layers
========================================================================================
"""

import os
import re
import sys
import math
import random
import logging
from datetime import datetime, timedelta, date
from functools import wraps
from typing import Dict, List, Any, Optional, Tuple, Union

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
    abort,
    make_response
)
from werkzeug.security import generate_password_hash, check_password_hash

# Local Relational Schema Models
from models import (
    db,
    User,
    Friend,
    Expense,
    HangoutSplit,
    Subscription
)

# Optional Google Gen AI SDK Integration for Live LLM Ingestion
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# ======================================================================================
# LOGGING & RUNTIME CONFIGURATION
# ======================================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [MintzCore] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("MintzWealthOS")


# ======================================================================================
# APPLICATION FACTORY & ENVIRONMENT INITIALIZATION
# ======================================================================================

app = Flask(__name__)

# Cryptographic Secret Key for HMAC-SHA256 Signed Session Cookies
app.secret_key = os.getenv(
    "MINTZ_SECRET_KEY",
    "mintz_wealth_os_production_secret_key_2026_genz_hackathon_elite"
)

# Template Engine Global Helper Bindings
app.jinja_env.globals.update(
    max=max,
    min=min,
    round=round,
    len=len,
    int=int,
    float=float,
    str=str
)

# Database Engine URI & ORM Parameters
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, "vibe_finance.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{database_path}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True
}

db.init_app(app)


# ======================================================================================
# GLOBAL FINANCIAL CONSTANTS & ACTUARIAL ASSUMPTIONS
# ======================================================================================

DAYS_IN_FINANCIAL_MONTH: int = 30
DEFAULT_ANNUAL_INFLATION_RATE: float = 0.060      # 6.0% Baseline Inflation
BENCHMARK_NIFTY_CAGR: float = 0.120               # 12.0% Broad Index Benchmark
MONTE_CARLO_SIMULATION_RUNS: int = 250            # Stochastic Walks Count
MINIMUM_SAFE_ALLOWANCE_FLOOR: float = 1.0         # Non-zero Denominator Clamp


# ======================================================================================
# SECTION 1: DETERMINISTIC VIBE HEALTH SCORE ENGINE (100-POINT MULTI-FACTOR MODEL)
# ======================================================================================

def compute_user_vibe_score(user: User) -> Dict[str, Any]:
    """
    Computes a real-time, deterministic 100-point financial health score across
    four mathematically isolated operational pillars:

      Pillar 1: Safe Spend Runway & Budget Burn Velocity (40 Max Points)
      Pillar 2: Systematic Target Savings Commitment Rate (25 Max Points)
      Pillar 3: Impulse vs. Value-Add Investment Outflow Ratio (20 Max Points)
      Pillar 4: Squad Debt Discipline & Hangout Tab Settlement (15 Max Points)

    Args:
        user (User): The authenticated SQLAlchemy User instance.

    Returns:
        Dict[str, Any]: Aggregate score, pillar sub-scores, status labels, CSS tokens,
                        and normalized monthly subscription overhead.
    """
    if not user:
        return {
            "total": 50,
            "budget_score": 20,
            "savings_score": 10,
            "impulse_score": 10,
            "debt_score": 10,
            "status_label": "Calibrating Telemetry ⏳",
            "status_color": "text-slate-400",
            "status_badge": "bg-slate-500/20 border-slate-500/30 text-slate-300",
            "recurring_sub_monthly": 0.0
        }

    user_subs: List[Subscription] = user.subscriptions or []
    user_expenses: List[Expense] = user.expenses or []
    user_splits: List[HangoutSplit] = user.splits or []

    # 1. Normalize Monthly Recurring Subscription Overhead
    recurring_sub_monthly = 0.0
    for sub in user_subs:
        if sub.billing_cycle == "Monthly":
            recurring_sub_monthly += float(sub.amount)
        elif sub.billing_cycle == "Yearly":
            recurring_sub_monthly += round(float(sub.amount) / 12.0, 2)
        else:
            recurring_sub_monthly += float(sub.amount)

    monthly_allowance = max(float(user.monthly_allowance or 5000.0), MINIMUM_SAFE_ALLOWANCE_FLOOR)
    target_savings = max(float(user.target_savings or 1000.0), 0.0)
    current_spent = max(float(user.current_spent or 0.0), 0.0)
    save_percentage = float(user.save_percentage or 20.0)

    spending_limit = max(monthly_allowance - target_savings, MINIMUM_SAFE_ALLOWANCE_FLOOR)
    effective_spent = current_spent + recurring_sub_monthly

    # ----------------------------------------------------------------------------------
    # PILLAR 1: BUDGET BURN VELOCITY (MAX 40 POINTS)
    # ----------------------------------------------------------------------------------
    if effective_spent <= 0:
        budget_score = 40
    elif effective_spent <= spending_limit * 0.50:
        budget_score = 40
    elif effective_spent <= spending_limit:
        # Scale linearly between 40 and 20 as spend moves from 50% to 100% of safe limit
        utilization_ratio = (effective_spent - (0.50 * spending_limit)) / (0.50 * spending_limit)
        budget_score = int(20 + (20 * (1.0 - utilization_ratio)))
    elif effective_spent <= monthly_allowance:
        # Over safe limit but within total monthly allowance (eating into savings target)
        savings_overage = effective_spent - spending_limit
        burn_into_savings_ratio = min(savings_overage / max(target_savings, 1.0), 1.0)
        budget_score = max(5, int(20 * (1.0 - burn_into_savings_ratio)))
    else:
        # Critical deficit - monthly allowance completely exhausted
        budget_score = 0

    # ----------------------------------------------------------------------------------
    # PILLAR 2: TARGET SAVINGS COMMITMENT RATE (MAX 25 POINTS)
    # ----------------------------------------------------------------------------------
    if save_percentage >= 30.0:
        savings_score = 25
    elif save_percentage >= 25.0:
        savings_score = 22
    elif save_percentage >= 20.0:
        savings_score = 20
    elif save_percentage >= 15.0:
        savings_score = 15
    elif save_percentage >= 10.0:
        savings_score = 10
    elif save_percentage >= 5.0:
        savings_score = 6
    else:
        savings_score = 2

    # ----------------------------------------------------------------------------------
    # PILLAR 3: IMPULSE VS. NEEDS EXPENDITURE RATIO (MAX 20 POINTS)
    # ----------------------------------------------------------------------------------
    bad_expenses_total = sum(float(e.amount) for e in user_expenses if e.status == "Bad")
    bad_subs_monthly = sum(
        float(s.amount) if s.billing_cycle == "Monthly" else round(float(s.amount) / 12.0, 2)
        for s in user_subs if s.status == "Bad"
    )
    total_impulse_drain = bad_expenses_total + bad_subs_monthly

    if effective_spent > 0:
        impulse_drain_ratio = min(total_impulse_drain / effective_spent, 1.0)
        impulse_score = max(0, int(20 * (1.0 - impulse_drain_ratio)))
    else:
        impulse_score = 20

    # ----------------------------------------------------------------------------------
    # PILLAR 4: SQUAD DEBT DISCIPLINE & UNSETTLED TABS (MAX 15 POINTS)
    # ----------------------------------------------------------------------------------
    unsettled_splits = [s for s in user_splits if s.status != "Settled (Paid)"]
    unsettled_count = len(unsettled_splits)

    if unsettled_count == 0:
        debt_score = 15
    elif unsettled_count == 1:
        debt_score = 12
    elif unsettled_count == 2:
        debt_score = 9
    elif unsettled_count <= 4:
        debt_score = 5
    else:
        debt_score = 2

    # Final Composite Summation & Clamping
    total_score = max(0, min(100, budget_score + savings_score + impulse_score + debt_score))

    # Dynamic Classification Badges
    if total_score >= 85:
        status_label = "Certified Wealth God 👑"
        status_color = "text-emerald-400"
        status_badge = "bg-emerald-500/20 border-emerald-500/30 text-emerald-300"
    elif total_score >= 70:
        status_label = "High Key Thriving ✨"
        status_color = "text-cyan-400"
        status_badge = "bg-cyan-500/20 border-cyan-500/30 text-cyan-300"
    elif total_score >= 50:
        status_label = "Walking on Thin Ice ⚠️"
        status_color = "text-amber-400"
        status_badge = "bg-amber-500/20 border-amber-500/30 text-amber-300"
    else:
        status_label = "Certified Cooked / Down Bad 💀"
        status_color = "text-rose-500"
        status_badge = "bg-rose-500/20 border-rose-500/30 text-rose-300"

    return {
        "total": total_score,
        "budget_score": budget_score,
        "savings_score": savings_score,
        "impulse_score": impulse_score,
        "debt_score": debt_score,
        "status_label": status_label,
        "status_color": status_color,
        "status_badge": status_badge,
        "recurring_sub_monthly": round(recurring_sub_monthly, 2)
    }


# ======================================================================================
# SECTION 2: ACTUARIAL SAVINGS VELOCITY & MONTE CARLO FORECASTING ENGINE
# ======================================================================================

def compute_savings_forecast(user: User) -> Dict[str, Any]:
    """
    Computes real-time spending velocity, month-end projected net savings,
    target bag completion dates, multi-horizon trajectories, and stochastic
    Monte Carlo goal attainment probabilities.

    Args:
        user (User): The active User database model.

    Returns:
        Dict[str, Any]: Structured numerical forecast payload for views and charts.
    """
    today_dt = date.today()
    day_of_month = max(today_dt.day, 1)
    days_in_month = DAYS_IN_FINANCIAL_MONTH
    days_remaining = max(days_in_month - day_of_month, 0)

    user_subs: List[Subscription] = user.subscriptions or []
    sub_monthly = sum(
        float(s.amount) if s.billing_cycle == "Monthly" else round(float(s.amount) / 12.0, 2)
        for s in user_subs
    )

    monthly_allowance = float(user.monthly_allowance or 5000.0)
    target_savings = float(user.target_savings or 1000.0)
    current_spent = float(user.current_spent or 0.0)
    goal_amount = max(float(user.goal_amount or 10000.0), MINIMUM_SAFE_ALLOWANCE_FLOOR)

    total_spent_effective = current_spent + sub_monthly
    daily_burn_rate = round(total_spent_effective / float(day_of_month), 2)
    projected_total_spend = round(total_spent_effective + (daily_burn_rate * days_remaining), 2)
    projected_month_savings = round(monthly_allowance - projected_total_spend, 2)

    # Goal Attainment Horizon Math
    if projected_month_savings > 0:
        months_needed = round(goal_amount / projected_month_savings, 1)
        projected_completion_days = int(months_needed * days_in_month)
        est_date = today_dt + timedelta(days=projected_completion_days)
        goal_eta_str = est_date.strftime("%B %Y")

        if projected_month_savings >= target_savings:
            forecast_status = "On Track 🚀"
        elif projected_month_savings >= target_savings * 0.75:
            forecast_status = "Paced Slower ⚠️"
        else:
            forecast_status = "Goal At Risk 🚨"
    else:
        months_needed = None
        goal_eta_str = "Delayed Indefinitely (Overspending) 💀"
        forecast_status = "Negative Cashflow 🚨"

    # Multi-Horizon Trajectory Model (6-Month Projection for Chart.js)
    trajectory_labels: List[str] = []
    ideal_trajectory: List[float] = []
    predicted_trajectory: List[float] = []
    pessimistic_trajectory: List[float] = []

    curr_ideal = 0.0
    curr_pred = 0.0
    curr_pessimistic = 0.0
    pred_monthly_flow = max(projected_month_savings, 0.0)
    pessimistic_flow = max(pred_monthly_flow * 0.70, 0.0)

    for i in range(1, 7):
        future_dt = today_dt + timedelta(days=i * days_in_month)
        trajectory_labels.append(future_dt.strftime("%b %y"))

        curr_ideal += target_savings
        curr_pred += pred_monthly_flow
        curr_pessimistic += pessimistic_flow

        ideal_trajectory.append(round(curr_ideal, 2))
        predicted_trajectory.append(round(curr_pred, 2))
        pessimistic_trajectory.append(round(curr_pessimistic, 2))

    # Stochastic Monte Carlo Goal Simulation (Random Gaussian Walks)
    planned_months = max(int(math.ceil(goal_amount / max(target_savings, 1.0))), 1)
    success_count = 0
    volatility_sigma = (
        0.18 if user.risk_profile == "Safe"
        else (0.28 if user.risk_profile == "Balanced" else 0.42)
    )

    for _ in range(MONTE_CARLO_SIMULATION_RUNS):
        sim_wealth = 0.0
        for _ in range(planned_months):
            stochastic_shock = random.gauss(0, volatility_sigma)
            simulated_flow = pred_monthly_flow * (1.0 + stochastic_shock)
            sim_wealth += max(simulated_flow, -0.20 * monthly_allowance)
        if sim_wealth >= goal_amount:
            success_count += 1

    monte_carlo_prob = round((success_count / float(MONTE_CARLO_SIMULATION_RUNS)) * 100.0, 1)

    return {
        "day_of_month": day_of_month,
        "days_remaining": days_remaining,
        "daily_burn_rate": daily_burn_rate,
        "projected_total_spend": projected_total_spend,
        "projected_month_savings": projected_month_savings,
        "planned_savings": target_savings,
        "months_needed": months_needed,
        "goal_eta_str": goal_eta_str,
        "forecast_status": forecast_status,
        "trajectory_labels": trajectory_labels,
        "ideal_trajectory": ideal_trajectory,
        "predicted_trajectory": predicted_trajectory,
        "pessimistic_trajectory": pessimistic_trajectory,
        "monte_carlo_prob": monte_carlo_prob
    }


# ======================================================================================
# SECTION 3: CYBER TAMAGOTCHI PET EVOLUTION & STATE ENGINE
# ======================================================================================

def compute_cyber_pet_state(user: User, vibe: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evolves the visual cyber pet mascot (Robo Cat, Cyber Dog, Mech Bot),
    battery health percentage, dialogue bubble quotes, and halo auras dynamically
    tied to the user's real-time Vibe Health Score.

    Args:
        user (User): The authenticated User model.
        vibe (Dict[str, Any]): Real-time computed vibe score payload.

    Returns:
        Dict[str, Any]: Mascot sprite, mood title, quote, battery stats, CSS aura styles.
    """
    score = vibe.get("total", 80)
    pet_type = getattr(user, "pet_type", "cat") or "cat"
    pet_name = getattr(user, "pet_name", "Byte") or "Byte"
    goal_name = getattr(user, "goal_name", "Emergency Bag") or "Emergency Bag"

    pet_sprites = {
        "cat": {
            "god": "👑 🐱 ⚡",
            "thriving": "😸 🎮",
            "ice": "😿 🧋",
            "cooked": "💀 🙀 🚨"
        },
        "dog": {
            "god": "👑 🐶 🚀",
            "thriving": "🐕 🦴",
            "ice": "🐕‍🦺 🌧️",
            "cooked": "💀 🐺 🚨"
        },
        "robot": {
            "god": "👑 🤖 💎",
            "thriving": "🦾 🤖 🔋",
            "ice": "🤖 ⚠️",
            "cooked": "💀 💥 🚨"
        }
    }

    species_pack = pet_sprites.get(pet_type, pet_sprites["cat"])

    if score >= 85:
        mood_title = "Ascended & High On Wealth 👑"
        avatar = species_pack["god"]
        quote = f"Purr-fect discipline! We are cruising toward your '{goal_name}' target bag at lightning speed!"
        aura_class = "border-emerald-500/50 shadow-emerald-500/30 bg-emerald-950/20"
        battery_level = 100
        battery_color = "bg-emerald-400"
    elif score >= 70:
        mood_title = "Vibing & Battery Full ✨"
        avatar = species_pack["thriving"]
        quote = f"Safe spend runway looks clean. Keep burn velocity under control and we hit '{goal_name}' easily!"
        aura_class = "border-cyan-500/50 shadow-cyan-500/30 bg-cyan-950/20"
        battery_level = 75
        battery_color = "bg-cyan-400"
    elif score >= 50:
        mood_title = "Nervous & Low Battery ⚠️"
        avatar = species_pack["ice"]
        quote = f"Hold up! Too many impulse swipes lately... our '{goal_name}' bag is getting pushed back!"
        aura_class = "border-amber-500/50 shadow-amber-500/30 bg-amber-950/20"
        battery_level = 40
        battery_color = "bg-amber-400"
    else:
        mood_title = "Critical Glitch & Battery Dead 💀"
        avatar = species_pack["cooked"]
        quote = "System overload! Overspending has completely drained my power core. Stop the takeout orders!"
        aura_class = "border-rose-500/60 shadow-rose-500/40 bg-rose-950/30 animate-pulse"
        battery_level = 15
        battery_color = "bg-rose-500"

    return {
        "pet_name": pet_name,
        "pet_type": pet_type,
        "avatar": avatar,
        "mood_title": mood_title,
        "quote": quote,
        "aura_class": aura_class,
        "battery_level": battery_level,
        "battery_color": battery_color
    }


# ======================================================================================
# SECTION 4: INDIAN BANKING MULTI-PATTERN REGEX SMS TOKENIZER
# ======================================================================================

CATEGORY_TAXONOMY: Dict[str, List[str]] = {
    "Dining Out": [
        "zomato", "swiggy", "starbucks", "mcdonalds", "kfc", "dominos", "pizza", "burger",
        "cafe", "boba", "chai", "diner", "restaurant", "eats", "bar", "brewery", "haldiram",
        "subway", "barbeque", "eatfit", "freshmenu", "chaayos", "faasos", "behrouz"
    ],
    "Groceries": [
        "blinkit", "zepto", "instamart", "bigbasket", "dmart", "spencer", "supermarket",
        "grocery", "nature basket", "milk", "vegetables", "kirana", "provisions", "jio mart"
    ],
    "Transit": [
        "uber", "ola", "rapido", "metro", "fuel", "petrol", "indian oil", "bharat petro",
        "hpcl", "shell", "fastag", "toll", "irctc", "redbus", "flight", "indigo", "makemytrip"
    ],
    "Education": [
        "udemy", "coursera", "book", "library", "college", "tuition", "stationery",
        "exam", "notion", "chatgpt", "openai", "github", "aws", "google cloud", "skillshare"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "ajio", "zara", "h&m", "uniqlo", "nykaa",
        "tata cliq", "electronics", "croma", "reliance digital", "apple", "shoes", "meesho"
    ]
}

def parse_bank_sms(sms_text: str) -> Dict[str, Any]:
    """
    Parses unstructured Indian banking SMS notifications and UPI debit strings
    (HDFC, SBI, ICICI, Axis, Kotak, Paytm, PhonePe, Google Pay, CRED) to extract
    exact transaction amounts, merchant entities, and automated AI value tags.

    Args:
        sms_text (str): Raw incoming SMS or payment notification text.

    Returns:
        Dict[str, Any]: Parsed metadata (title, amount, category, status, verdict, validity).
    """
    cleaned_text = sms_text.strip()
    amount = 0.0

    # Multi-Pattern Amount Extraction Regex
    amount_patterns = [
        r'(?:Rs\.?|INR|₹)\s*([\d,]+(?:\.\d{1,2})?)',
        r'(?:debited\s*(?:by|for|with)?)\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d{1,2})?)',
        r'(?:spent|paid|vpa)\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d{1,2})?)',
        r'(?:transfer(?:red)?\s*(?:of)?)\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d{1,2})?)'
    ]

    for pattern in amount_patterns:
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            try:
                amount_str = match.group(1).replace(",", "")
                amount = float(amount_str)
                break
            except ValueError:
                continue

    # Multi-Pattern Merchant Entity Extraction Regex
    merchant = "UPI Transaction"
    merchant_patterns = [
        r'(?:to|at|info\/|vpa|paid to|trf to)\s+([A-Za-z0-9\s\.\@\-\&]+?)(?:\s+on|\s+via|\s+ref|\s+upi|\.|\,|$)',
        r'(?:towards|in favor of)\s+([A-Za-z0-9\s\.\@\-\&]+?)(?:\s+on|\s+via|\.|$)',
        r'(?:sent to)\s+([A-Za-z0-9\s\.\@\-\&]+?)(?:\s+on|\.|$)'
    ]

    for pattern in merchant_patterns:
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            merchant = match.group(1).strip()
            break

    # Categorical Taxonomy Matching & W/L Classification
    token_corpus = (merchant + " " + cleaned_text).lower()
    matched_category = "Shopping"

    for cat_name, keywords in CATEGORY_TAXONOMY.items():
        if any(keyword in token_corpus for keyword in keywords):
            matched_category = cat_name
            break

    if matched_category in ["Dining Out", "Shopping"]:
        status = "Bad"
        ai_verdict = (
            "Instant Craving Burn 🍕" if matched_category == "Dining Out"
            else "Impulse Bag Delay 🛍️"
        )
    else:
        status = "Good"
        if matched_category == "Education":
            ai_verdict = "Brain Gains Investment 🧠"
        elif matched_category == "Groceries":
            ai_verdict = "Valid Nutrition Restock 🥦"
        else:
            ai_verdict = "Essential Transit Move 🚗"

    return {
        "title": merchant[:45],
        "amount": amount,
        "category": matched_category,
        "status": status,
        "ai_verdict": ai_verdict,
        "is_valid": amount > 0.0
    }


# ======================================================================================
# SECTION 5: FINBRO GEN Z AI PERSONA & CONTEXT INGESTION AGENT
# ======================================================================================

def get_finbro_ai_response(
    user: User,
    vibe: Dict[str, Any],
    forecast: Dict[str, Any],
    prompt: str,
    persona_mode: str = "roast"
) -> str:
    """
    Evaluates user prompts inside the FinBro engine, injecting real-time database
    financial metrics, daily burn velocity, and active persona directives.

    Args:
        user (User): The authenticated User instance.
        vibe (Dict[str, Any]): Real-time computed vibe score payload.
        forecast (Dict[str, Any]): Actuarial forecasting payload.
        prompt (str): User input string.
        persona_mode (str): Directive ('roast', 'hype', 'guru').

    Returns:
        str: FinBro conversational verdict.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    persona_directives = {
        "roast": (
            "Deliver brutally funny, savage Gen Z roasts with slang (cooked, L, mid, fr fr, down bad). "
            "Call out unnecessary spending directly and roast their daily burn rate."
        ),
        "hype": (
            "Act as an energetic hype-man. Celebrate savings wins, validate smart budgeting moves, "
            "and motivate the user toward their goals with peak energy."
        ),
        "guru": (
            "Provide concise, mathematically sound financial advice focusing on compounding, SIPs, "
            "and index funds without corporate jargon."
        )
    }

    safe_allowance_left = max(
        float(user.monthly_allowance or 5000.0) - float(user.target_savings or 1000.0) - float(user.current_spent or 0.0),
        0.0
    )

    system_instruction = f"""
    You are FinBro, an AI wealth advisor inside the Gen Z personal finance app Mintz.

    USER REAL-TIME TELEMETRY:
    - User Name: {user.name}
    - Target Bag: {user.goal_name} (Total Cost: ₹{user.goal_amount})
    - Monthly Inflow: ₹{user.monthly_allowance}
    - Target Savings: ₹{user.target_savings} ({user.save_percentage}%)
    - Safe Spend Runway Remaining: ₹{safe_allowance_left}
    - Current Total Outflow: ₹{user.current_spent}
    - Daily Burn Velocity: ₹{forecast.get('daily_burn_rate', 0)}/day
    - Goal Completion ETA: {forecast.get('goal_eta_str', 'N/A')} ({forecast.get('forecast_status', 'Active')})
    - Vibe Health Score: {vibe.get('total', 80)}/100 ({vibe.get('status_label', 'Active')})
    - Fixed Auto-Sub Drain: ₹{vibe.get('recurring_sub_monthly', 0)}/month
    - Risk Profile: {user.risk_profile}

    DIRECTIVE: {persona_directives.get(persona_mode, persona_directives['roast'])}

    OUTPUT RULES:
    1. Maximum 2-4 punchy sentences.
    2. Incorporate user's live numbers (burn rate, goal name, or safe runway) naturally.
    3. Maintain Indian Rupee (₹) context and Gen Z vernacular.
    """

    if GENAI_AVAILABLE and api_key:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.75,
                    max_output_tokens=250
                )
            )
            if response and response.text:
                return response.text.strip()
        except Exception as exc:
            logger.warning(f"Gemini API invocation exception: {exc}")

    # Heuristic Fallback Engine
    prompt_lower = prompt.lower()
    burn_rate = forecast.get("daily_burn_rate", 0)
    goal_name = user.goal_name
    score_val = vibe.get("total", 80)
    eta_val = forecast.get("goal_eta_str", "soon")

    if persona_mode == "roast":
        if any(keyword in prompt_lower for keyword in ["zomato", "swiggy", "food", "takeout", "biryani", "eat", "pizza"]):
            return (
                f"Bro, you're burning ₹{burn_rate}/day and your Vibe Score is {score_val}/100. "
                f"That takeout order is pushing your '{goal_name}' bag into next semester fr fr 💀."
            )
        elif any(keyword in prompt_lower for keyword in ["sub", "subscription", "netflix", "spotify", "prime"]):
            sub_drain = vibe.get("recurring_sub_monthly", 0)
            return (
                f"You're leaking ₹{sub_drain}/month on autopilot subscriptions. "
                f"Cancel those ghost subs before checking out more carts 🚨."
            )
        elif any(keyword in prompt_lower for keyword in ["invest", "sip", "stocks", "market"]):
            return (
                f"Thinking about investing while spending at ₹{burn_rate}/day? "
                f"Fix that daily cash leak first before acting like a Dalal Street mogul 💀."
            )
        else:
            return (
                f"Yo {user.name}, you've already burned ₹{user.current_spent} this month. "
                f"Stop making spontaneous swipes if you actually want that ₹{user.goal_amount} '{goal_name}' bag!"
            )
    elif persona_mode == "hype":
        if any(keyword in prompt_lower for keyword in ["invest", "sip", "save", "goal"]):
            return (
                f"Major W behavior {user.name}! Automating ₹{user.target_savings} into index funds locks in compounding wealth. "
                f"You're unlocking '{goal_name}' early 🚀✨!"
            )
        else:
            return (
                f"Yo {user.name}! Your ₹{user.target_savings} auto-savings target is locked in! "
                f"Keep daily burn near ₹{burn_rate} and you unlock '{goal_name}' by {eta_val}! Let's get this bag 🚀✨."
            )
    else:  # guru
        if any(keyword in prompt_lower for keyword in ["invest", "sip", "nifty", "stock", "etf"]):
            return (
                f"With your '{user.risk_profile}' profile, automating a ₹500–₹1,000 monthly SIP into Nifty 50 index funds "
                f"accelerates your runway and yields reliable 12% benchmark returns over college."
            )
        else:
            daily_limit = round((float(user.monthly_allowance or 5000.0) - float(user.target_savings or 1000.0)) / 30.0, 2)
            return (
                f"Keep your daily burn velocity under ₹{daily_limit} to preserve your monthly target of ₹{user.target_savings} on schedule."
            )


# ======================================================================================
# SECTION 6: AUTHENTICATION GUARDS & CONTEXT PROCESSORS
# ======================================================================================

@app.context_processor
def inject_current_user():
    """Injects user authentication state and live Vibe score across all Jinja2 templates."""
    if "user_id" in session:
        user_id = session.get("user_id")
        user = db.session.get(User, user_id)
        if user:
            vibe = compute_user_vibe_score(user)
            user.health_score = vibe["total"]
            return {"current_user": user, "vibe": vibe}
    return {"current_user": None, "vibe": None}

def login_required(f):
    """Guards protected routes against unauthenticated sessions and incomplete onboarding."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Log in to check your financial vibes.", "warning")
            return redirect(url_for("login"))
        user = db.session.get(User, session["user_id"])
        if not user:
            session.clear()
            return redirect(url_for("login"))
        if not user.onboarding_complete:
            allowed_endpoints = [
                "onboarding_step1",
                "onboarding_step2",
                "onboarding_step3",
                "onboarding_step4",
                "logout"
            ]
            if request.endpoint not in allowed_endpoints:
                return redirect(url_for("onboarding_step1"))
        return f(*args, **kwargs)
    return decorated_function


# ======================================================================================
# SECTION 7: USER AUTHENTICATION & ONBOARDING PIPELINE
# ======================================================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handles new user registration with password hashing."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")
        name = request.form.get("name", "").strip()

        if not email or not password or not name:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("signup"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in!", "danger")
            return redirect(url_for("login"))

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            onboarding_complete=False,
            current_spent=0.0,
            streak_count=1,
            pet_type="cat",
            pet_name="Byte"
        )
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        logger.info(f"New user registered: {email} (ID: {new_user.id})")
        return redirect(url_for("onboarding_step1"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Authenticates existing user credentials and increments daily active streak."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            today_str = date.today().strftime("%Y-%m-%d")
            if user.last_active_date != today_str:
                user.streak_count = (user.streak_count or 0) + 1
                user.last_active_date = today_str
                db.session.commit()

            logger.info(f"User login successful: {email} (Streak: {user.streak_count}d)")
            if not user.onboarding_complete:
                return redirect(url_for("onboarding_step1"))
            return redirect(url_for("dashboard"))

        flash("Invalid email or password. Please try again.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Terminates active session."""
    user_id = session.pop("user_id", None)
    logger.info(f"User session terminated (ID: {user_id})")
    return redirect(url_for("login"))

@app.route("/onboard/step-1", methods=["GET", "POST"])
def onboarding_step1():
    """Step 1: Primary Target Bag & Capital Goal Configuration."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = db.session.get(User, session["user_id"])
    if request.method == "POST":
        user.goal_name = request.form.get("goal_name", "Emergency Bag").strip() or "Emergency Bag"
        user.goal_amount = float(request.form.get("goal_amount", 10000))
        db.session.commit()
        return redirect(url_for("onboarding_step2"))
    return render_template("onboarding_1.html", user=user)

@app.route("/onboard/step-2", methods=["GET", "POST"])
def onboarding_step2():
    """Step 2: Monthly Inflow & Allowance Baseline."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = db.session.get(User, session["user_id"])
    if request.method == "POST":
        user.monthly_allowance = float(request.form.get("monthly_allowance", 5000))
        db.session.commit()
        return redirect(url_for("onboarding_step3"))
    return render_template("onboarding_2.html", user=user)

@app.route("/onboard/step-3", methods=["GET", "POST"])
def onboarding_step3():
    """Step 3: Systematic Auto-Savings Rate Allocation."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = db.session.get(User, session["user_id"])
    if request.method == "POST":
        pct = float(request.form.get("save_percentage", 20))
        user.save_percentage = pct
        user.target_savings = (float(user.monthly_allowance) * pct) / 100.0
        db.session.commit()
        return redirect(url_for("onboarding_step4"))
    return render_template("onboarding_3.html", user=user)

@app.route("/onboard/step-4", methods=["GET", "POST"])
def onboarding_step4():
    """Step 4: Investment Persona Profile & Dashboard Finalization."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = db.session.get(User, session["user_id"])
    if request.method == "POST":
        user.risk_profile = request.form.get("risk_profile", "Balanced")
        user.onboarding_complete = True
        vibe = compute_user_vibe_score(user)
        user.health_score = vibe["total"]
        db.session.commit()
        flash("Financial Dashboard Initialized! 🚀", "success")
        return redirect(url_for("dashboard"))
    return render_template("onboarding_4.html", user=user)


# ======================================================================================
# SECTION 8: CORE DASHBOARD & CASHFLOW CALENDAR
# ======================================================================================

@app.route("/")
@login_required
def dashboard():
    """Main executive overview: cashflow metrics, weekly calendar, and active subs."""
    user = db.session.get(User, session["user_id"])
    vibe = compute_user_vibe_score(user)
    user.health_score = vibe["total"]
    db.session.commit()

    forecast_data = compute_savings_forecast(user)
    pet_data = compute_cyber_pet_state(user, vibe)
    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.created_at.desc()).all()
    splits = HangoutSplit.query.filter_by(user_id=user.id).order_by(HangoutSplit.created_at.desc()).all()
    subs = Subscription.query.filter_by(user_id=user.id).order_by(Subscription.created_at.desc()).all()
    spending_limit = round(float(user.monthly_allowance) - float(user.target_savings), 2)

    # 7-Day Live Rolling Calendar Window
    today_dt = date.today()
    calendar_days = []
    for i in range(6, -1, -1):
        day_date = today_dt - timedelta(days=i)
        day_str = day_date.strftime("%Y-%m-%d")
        day_spends = [e for e in expenses if e.date == day_str]
        total_for_day = sum(float(e.amount) for e in day_spends)

        calendar_days.append({
            "day_name": day_date.strftime("%a"),
            "day_num": day_date.strftime("%d"),
            "date_str": day_str,
            "is_today": (i == 0),
            "expenses": day_spends,
            "total_spent": total_for_day
        })

    return render_template(
        "dashboard.html",
        user=user,
        vibe=vibe,
        pet=pet_data,
        forecast=forecast_data,
        expenses=expenses,
        splits=splits,
        subscriptions=subs,
        spending_limit=spending_limit,
        calendar_days=calendar_days
    )


# ======================================================================================
# SECTION 9: GOALS & PREDICTIVE FINFIT ENGINES
# ======================================================================================

@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    """Allows users to adjust target bags, monthly allowance, and savings rates."""
    user = db.session.get(User, session["user_id"])
    if request.method == "POST":
        user.goal_name = request.form.get("goal_name", user.goal_name).strip() or user.goal_name
        user.goal_amount = float(request.form.get("goal_amount", user.goal_amount))
        user.monthly_allowance = float(request.form.get("monthly_allowance", user.monthly_allowance))
        user.save_percentage = float(request.form.get("save_percentage", user.save_percentage))
        user.risk_profile = request.form.get("risk_profile", user.risk_profile)
        user.target_savings = round((user.monthly_allowance * user.save_percentage) / 100.0, 2)

        vibe = compute_user_vibe_score(user)
        user.health_score = vibe["total"]
        db.session.commit()
        flash("Financial targets updated successfully! ✨", "success")
        return redirect(url_for("goals"))

    spending_limit = round(float(user.monthly_allowance) - float(user.target_savings), 2)
    return render_template("goals.html", user=user, spending_limit=spending_limit)

@app.route("/forecast")
@login_required
def forecast():
    """FinFit: Displays 6-month trajectory graphs and Monte Carlo simulations."""
    user = db.session.get(User, session["user_id"])
    forecast_data = compute_savings_forecast(user)
    return render_template("forecast.html", user=user, f=forecast_data)


# ======================================================================================
# SECTION 10: CYBER PET COMPANION MANAGEMENT
# ======================================================================================

@app.route("/update-pet", methods=["POST"])
@login_required
def update_pet():
    """Updates user mascot avatar species (cat/dog/robot) and custom pet nickname."""
    user = db.session.get(User, session["user_id"])
    pet_type = request.form.get("pet_type", "cat")
    pet_name = request.form.get("pet_name", "Byte").strip() or "Byte"

    user.pet_type = pet_type
    user.pet_name = pet_name
    db.session.commit()

    logger.info(f"User {user.id} updated pet: {pet_name} ({pet_type})")
    flash(f"⚡ Cyber Pet updated to {pet_name} ({pet_type.upper()})!", "success")
    return redirect(url_for("dashboard"))


# ======================================================================================
# SECTION 11: FINBRO AI CHAT & ASYNC API ENDPOINTS
# ======================================================================================

@app.route("/advisor", methods=["GET", "POST"])
@login_required
def advisor():
    """Dedicated standalone view for FinBro AI with persona selection."""
    user = db.session.get(User, session["user_id"])
    vibe = compute_user_vibe_score(user)
    f = compute_savings_forecast(user)

    bot_reply = None
    active_mode = "roast"
    user_prompt = ""

    if request.method == "POST":
        user_prompt = request.form.get("prompt", "").strip()
        active_mode = request.form.get("persona_mode", "roast")
        if user_prompt:
            bot_reply = get_finbro_ai_response(user, vibe, f, user_prompt, active_mode)

    return render_template(
        "advisor.html",
        user=user,
        vibe=vibe,
        f=f,
        bot_reply=bot_reply,
        active_mode=active_mode,
        user_prompt=user_prompt
    )

@app.route("/api/finbro-chat", methods=["POST"])
@login_required
def api_finbro_chat():
    """Asynchronous JSON API for floating bottom-right FinBro chat orb."""
    user = db.session.get(User, session["user_id"])
    vibe = compute_user_vibe_score(user)
    f = compute_savings_forecast(user)

    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()
    persona_mode = data.get("persona_mode", "roast")

    if not prompt:
        return jsonify({"reply": "Bro, say something! Don't leave me on read 💀."})

    reply = get_finbro_ai_response(user, vibe, f, prompt, persona_mode)
    return jsonify({
        "reply": reply,
        "vibe_score": vibe["total"],
        "burn_rate": f["daily_burn_rate"]
    })


# ======================================================================================
# SECTION 12: TRACKY & AUTO-INGESTION PIPELINES
# ======================================================================================

@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    """Manual and automated expense logger with live ledger feed."""
    user = db.session.get(User, session["user_id"])
    if request.method == "POST":
        title = request.form.get("title", "").strip() or "Expense"
        amount = float(request.form.get("amount", 0))
        category = request.form.get("category", "Shopping")

        status = "Bad" if category in ["Dining Out", "Shopping", "Entertainment"] else "Good"
        verdict = "Delaying the Goal 🚨" if status == "Bad" else "Valid Essential Move ✨"

        new_exp = Expense(
            user_id=user.id,
            title=title,
            amount=amount,
            category=category,
            ai_verdict=verdict,
            status=status,
            date=date.today().strftime("%Y-%m-%d")
        )
        db.session.add(new_exp)
        user.current_spent = round(float(user.current_spent or 0.0) + amount, 2)

        vibe = compute_user_vibe_score(user)
        user.health_score = vibe["total"]
        db.session.commit()
        return redirect(url_for("tracker"))

    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.created_at.desc()).all()
    return render_template("tracker.html", user=user, expenses=expenses)

@app.route("/auto-sync", methods=["POST"])
@login_required
def auto_sync():
    """Parses raw bank SMS or simulated bank webhooks into expense records."""
    user = db.session.get(User, session["user_id"])
    sync_mode = request.form.get("sync_mode")

    if sync_mode == "sms_parse":
        raw_sms = request.form.get("raw_sms", "")
        parsed = parse_bank_sms(raw_sms)
        if parsed["is_valid"]:
            new_exp = Expense(
                user_id=user.id,
                title=parsed["title"],
                amount=parsed["amount"],
                category=parsed["category"],
                ai_verdict=parsed["ai_verdict"],
                status=parsed["status"],
                date=date.today().strftime("%Y-%m-%d")
            )
            db.session.add(new_exp)
            user.current_spent = round(float(user.current_spent or 0.0) + parsed["amount"], 2)

            vibe = compute_user_vibe_score(user)
            user.health_score = vibe["total"]
            db.session.commit()
            flash(f"⚡ Ingested: ₹{parsed['amount']} to {parsed['title']}", "success")
        else:
            flash("Could not parse transaction amount from SMS text.", "danger")
    elif sync_mode == "bank_simulate":
        new_exp = Expense(
            user_id=user.id,
            title="Swiggy Late Night",
            amount=340.0,
            category="Dining Out",
            ai_verdict="Midnight Munchies L 🚨",
            status="Bad",
            date=date.today().strftime("%Y-%m-%d")
        )
        db.session.add(new_exp)
        user.current_spent = round(float(user.current_spent or 0.0) + 340.0, 2)

        vibe = compute_user_vibe_score(user)
        user.health_score = vibe["total"]
        db.session.commit()
        flash("⚡ Synced simulated transaction from Bank!", "success")

    return redirect(url_for("tracker"))


# ======================================================================================
# SECTION 13: AUTO-SUBSCRIPTIONS & OVERHEAD LEAK AUDITOR
# ======================================================================================

@app.route("/add-subscription", methods=["POST"])
@login_required
def add_subscription():
    """Registers a recurring auto-subscription with automated value classification."""
    user = db.session.get(User, session["user_id"])
    title = request.form.get("title", "").strip() or "Subscription"
    amount = float(request.form.get("amount", 0))
    billing_cycle = request.form.get("billing_cycle", "Monthly")
    category = request.form.get("category", "Entertainment / OTT")
    renewal_day = request.form.get("renewal_day", "1st of month")

    cat_lower = (category + " " + title).lower()
    productive_keywords = [
        "gym", "fitness", "ai", "chatgpt", "notion", "course",
        "study", "books", "cloud", "github", "cult"
    ]

    if any(keyword in cat_lower for keyword in productive_keywords):
        status = "Good"
        verdict = "Valid W Investment 🧠"
    else:
        status = "Bad"
        verdict = "Recurring Sub Trap / Potential L 🚨"

    new_sub = Subscription(
        user_id=user.id,
        title=title,
        amount=amount,
        billing_cycle=billing_cycle,
        category=category,
        renewal_day=renewal_day,
        status=status,
        ai_verdict=verdict
    )
    db.session.add(new_sub)

    monthly_cost = amount if billing_cycle == "Monthly" else round(amount / 12.0, 2)
    new_exp = Expense(
        user_id=user.id,
        title=f"Auto-Sub: {title}",
        amount=monthly_cost,
        category=category,
        ai_verdict=verdict,
        status=status,
        date=date.today().strftime("%Y-%m-%d")
    )
    db.session.add(new_exp)

    vibe = compute_user_vibe_score(user)
    user.health_score = vibe["total"]
    db.session.commit()
    flash(f"⚡ Auto-Sub '{title}' Active ({verdict})", "success")
    return redirect(url_for("dashboard"))

@app.route("/cancel-subscription/<int:sub_id>", methods=["POST"])
@login_required
def cancel_subscription(sub_id: int):
    """Deletes active subscription and frees up recurring monthly allocation."""
    user = db.session.get(User, session["user_id"])
    sub = Subscription.query.filter_by(id=sub_id, user_id=user.id).first()
    if sub:
        db.session.delete(sub)
        vibe = compute_user_vibe_score(user)
        user.health_score = vibe["total"]
        db.session.commit()
        flash("Subscription canceled and monthly burn freed up! 💰", "success")
    return redirect(url_for("dashboard"))


# ======================================================================================
# SECTION 14: BUCKSIQ (OPPORTUNITY COST & SPEND INTELLIGENCE)
# ======================================================================================

@app.route("/intelligence")
@login_required
def intelligence():
    """BucksIQ: Evaluates W vs. L spending ratios, goal delays, and category drains."""
    user = db.session.get(User, session["user_id"])
    vibe = compute_user_vibe_score(user)
    f = compute_savings_forecast(user)
    expenses = Expense.query.filter_by(user_id=user.id).all()

    good_total = sum(float(e.amount) for e in expenses if e.status == "Good")
    bad_total = sum(float(e.amount) for e in expenses if e.status == "Bad")

    daily_savings_rate = max((float(user.target_savings or 1000.0) / 30.0), 1.0)
    days_delayed = round(bad_total / daily_savings_rate, 1) if bad_total > 0 else 0.0

    cat_map: Dict[str, float] = {}
    for e in expenses:
        cat_map[e.category] = cat_map.get(e.category, 0.0) + float(e.amount)

    cat_labels = list(cat_map.keys()) if cat_map else ["No Spends Yet"]
    cat_values = list(cat_map.values()) if cat_map else [0.0]

    return render_template(
        "intelligence.html",
        user=user,
        vibe=vibe,
        forecast=f,
        expenses=expenses,
        good_total=good_total,
        bad_total=bad_total,
        days_delayed=days_delayed,
        cat_labels=cat_labels,
        cat_values=cat_values
    )


# ======================================================================================
# SECTION 15: DUDESY (SOCIAL SQUAD BILL-SPLITTING)
# ======================================================================================

@app.route("/hangout-split", methods=["GET", "POST"])
@login_required
def hangout_split():
    """Dudesy: Calculates split bills, squad receivables, and friend UPI directories."""
    user = db.session.get(User, session["user_id"])
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_friend":
            name = request.form.get("name", "").strip()
            upi_id = request.form.get("upi_id", "").strip()
            if name:
                new_f = Friend(user_id=user.id, name=name, upi_id=upi_id)
                db.session.add(new_f)
                db.session.commit()
                flash(f"Added {name} to squad!", "success")
        elif action == "create_split":
            title = request.form.get("title", "").strip() or "Hangout Bill"
            total = float(request.form.get("total", 0))
            f_list = [f.strip() for f in request.form.get("friends", "").split(",") if f.strip()]
            share = round(total / (len(f_list) + 1), 2)
            owed = round(total - share, 2)

            new_split = HangoutSplit(
                user_id=user.id,
                title=title,
                total=total,
                paid_by="You",
                friends_list=", ".join(f_list),
                your_share=share,
                owed_to_you=owed,
                status="Unsettled"
            )
            db.session.add(new_split)

            vibe = compute_user_vibe_score(user)
            user.health_score = vibe["total"]
            db.session.commit()
            flash(f"Split ₹{total} logged!", "success")
        elif action == "settle":
            s_id = int(request.form.get("split_id"))
            split_obj = HangoutSplit.query.filter_by(id=s_id, user_id=user.id).first()
            if split_obj:
                split_obj.status = "Settled (Paid)"
                vibe = compute_user_vibe_score(user)
                user.health_score = vibe["total"]
                db.session.commit()
                flash("Tab marked settled! 💰", "success")
        return redirect(url_for("hangout_split"))

    splits = HangoutSplit.query.filter_by(user_id=user.id).order_by(HangoutSplit.created_at.desc()).all()
    friends = Friend.query.filter_by(user_id=user.id).all()
    return render_template("hangout_split.html", splits=splits, friends=friends, user=user)


# ======================================================================================
# SECTION 16: STONKS (MICRO-SIP) & HEALTH SCORE BREAKDOWNS
# ======================================================================================

@app.route("/investments")
@login_required
def investments():
    """Stonks: Interactive micro-SIP compounding calculator (12% Nifty 50 benchmark)."""
    user = db.session.get(User, session["user_id"])
    return render_template("investments.html", user=user)

@app.route("/health-score")
@login_required
def health_score():
    """Provides pillar-by-pillar diagnostics for the 100-point Vibe score."""
    user = db.session.get(User, session["user_id"])
    vibe = compute_user_vibe_score(user)
    return render_template("health_score.html", user=user, vibe=vibe)


# ======================================================================================
# SECTION 17: HTTP ERROR HANDLERS & STATUS CODES
# ======================================================================================

@app.errorhandler(404)
def error_not_found(e):
    """Custom 404 handler returning to main dashboard."""
    return render_template("base.html"), 404

@app.errorhandler(500)
def error_server_fault(e):
    """Custom 500 handler returning graceful JSON or fallback view."""
    logger.error(f"Internal server fault triggered: {e}")
    return jsonify({"error": "Internal Wealth OS anomaly. Safe mode engaged."}), 500


# ======================================================================================
# SECTION 18: SERVER ENTRYPOINT & DATABASE BOOTSTRAP
# ======================================================================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logger.info("SQLAlchemy relational tables verified & database ready.")
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
        use_reloader=True
    )