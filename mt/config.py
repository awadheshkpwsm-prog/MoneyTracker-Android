# ==========================================================
# MONEY TRACKER - ANDROID CONFIGURATION ADAPTER
# ==========================================================
import os

# On Android, keep user data in the app's writable data directory.
# The build wrapper sets MONEY_TRACKER_DATA_DIR to App.user_data_dir.
ANDROID_DATA_DIR = os.environ.get("MONEY_TRACKER_DATA_DIR")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = ANDROID_DATA_DIR or os.path.join(BASE_DIR, "data")
BACKUP_FOLDER = os.path.join(DATA_FOLDER, "Backups")
PDF_FOLDER = os.path.join(DATA_FOLDER, "MoneyTracker_Exports")
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)
TRANSACTION_FILE = os.path.join(DATA_FOLDER, "transactions.json")
BUDGET_FILE = os.path.join(DATA_FOLDER, "monthly_budgets.json")
CATEGORY_BUDGET_FILE = os.path.join(DATA_FOLDER, "category_budgets.json")
LOAN_FILE = os.path.join(DATA_FOLDER, "loans.json")
CURRENCY_FILE = os.path.join(DATA_FOLDER, "currency_settings.json")
ACCOUNT_FILE = os.path.join(DATA_FOLDER, "accounts.json")
LEGACY_FILES = {
    TRANSACTION_FILE: os.path.join(BASE_DIR, "transactions.json"),
    BUDGET_FILE: os.path.join(BASE_DIR, "budget.json"),
    CATEGORY_BUDGET_FILE: os.path.join(BASE_DIR, "category_budgets.json"),
    LOAN_FILE: os.path.join(BASE_DIR, "loans.json"),
    CURRENCY_FILE: os.path.join(BASE_DIR, "currency_settings.json"),
}
