import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import os
import logging
from flask import Flask
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db   # ✅ new import

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///fraud_detection.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize DB
db.init_app(app)

# ✅ Import models AFTER db.init_app
from models import Transaction, FraudAlert

# ✅ Create tables inside app context
with app.app_context():
    db.create_all()

# ✅ routes sabse last me import honge
import routes
