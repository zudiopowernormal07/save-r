"""
Save Restricted Content Bot Configuration

Developed by: LastPerson07XRexBots
Telegram: @RexBots_Official X @THEUPDATEDGUYS

Please retain this credit if you use or modify this project.
"""

import os


# ==============================
# Telegram Bot Credentials
# ==============================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8231199817:AAEEE4nU0zEr4fh8eNoiQr3M0RKjp8JrawU")
API_ID = int(os.environ.get("API_ID", "28389286"))
API_HASH = os.environ.get("API_HASH", "b88da5f4f338cca30f8ea5fb53cb083b")


# ==============================
# Admin Configuration
# ==============================

# Add admin user IDs separated by commas in environment variables
ADMINS = [int(admin) for admin in os.environ.get("ADMINS", "6334323103").split(",") if admin]


# ==============================
# Database Configuration
# ==============================

DB_URI = os.environ.get("DB_URI", "mongodb+srv://divyanshshukla5375_db_user:1kZ2dsVTktdMljpr@cluster0.lo5qk5v.mongodb.net/?appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "divyanshshukla5375_db_user")


# ==============================
# Logging Configuration
# ==============================

# Replace with your Telegram log channel ID (example: -1001234567890)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003268928688"))


# ==============================
# Error Handling
# ==============================

# Set to True to send error messages to users
ERROR_MESSAGE = os.environ.get("ERROR_MESSAGE", "True").lower() == "true"
