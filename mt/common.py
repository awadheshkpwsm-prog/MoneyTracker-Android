# ==========================================================
# MONEY TRACKER - SHARED STATE / DATA COMPATIBILITY
# ==========================================================
from config import *
from storage import load_json, save_json
from datetime import datetime

# Use the centralized paths from config.py.
# Keeping one source of truth prevents transactions/loans/budgets
# from being saved in the wrong directory.
FILE_NAME = TRANSACTION_FILE
# config.BUDGET_FILE is the canonical monthly budget file.
# Legacy root-level budget.json is migrated automatically by storage.py.
BUDGET_FILE = BUDGET_FILE
CATEGORY_BUDGET_FILE = CATEGORY_BUDGET_FILE
LOAN_FILE = LOAN_FILE
PDF_FOLDER = PDF_FOLDER

EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Rent",
    "Medical",
    "Entertainment",
    "Education",
    "Other"
]

INCOME_CATEGORIES = [
    "Salary",
    "Business",
    "Freelance",
    "Bonus",
    "Other"
]

transactions = load_json(TRANSACTION_FILE, [])

budgets = load_json(BUDGET_FILE, {})

category_budgets = load_json(
    CATEGORY_BUDGET_FILE,
    {}
)

loans = load_json(
    LOAN_FILE,
    []
)
if not isinstance(transactions, list):

    transactions = []

if not isinstance(budgets, dict):

    budgets = {}

if not isinstance(category_budgets, dict):

    category_budgets = {}

if not isinstance(loans, list):

    loans = []

transaction_id_changed = False
used_transaction_ids = set()
next_old_id = 1

for t in transactions:

    if not isinstance(t, dict):

        continue

    if "category" not in t:

        t["category"] = "Uncategorized"

    if "date" not in t:

        t["date"] = "Old Transaction"

    if "description" not in t:

        t["description"] = ""

    if "type" not in t:

        t["type"] = "Expense"

    if "amount" not in t:

        t["amount"] = 0

    existing_id = str(
        t.get("id", "")
    )

    if (
        not existing_id
        or existing_id in used_transaction_ids
    ):

        while (
            f"TXN-{next_old_id:04d}"
            in used_transaction_ids
        ):

            next_old_id += 1

        t["id"] = (
            f"TXN-{next_old_id:04d}"
        )

        used_transaction_ids.add(
            t["id"]
        )

        next_old_id += 1

        transaction_id_changed = True

    else:

        used_transaction_ids.add(
            existing_id
        )

if transaction_id_changed:

    save_json(TRANSACTION_FILE, transactions)

for loan in loans:

    if "name" not in loan:

        loan["name"] = "Unknown"

    if "type" not in loan:

        loan["type"] = "Lending"

    if "amount" not in loan:

        loan["amount"] = 0

    if "remaining" not in loan:

        loan["remaining"] = loan.get(
            "amount",
            0
        )

    if "date" not in loan:

        loan["date"] = "Old Loan"

    if "description" not in loan:

        loan["description"] = ""

    if "repayments" not in loan:

        loan["repayments"] = []


# ==========================================================
# MULTI-CURRENCY STATE / COMPATIBILITY
# ==========================================================
CURRENCY_FILE = CURRENCY_FILE
currency_settings = load_json(
    CURRENCY_FILE,
    {
        "base_currency": "MYR",
        "rates": {"MYR": 1.0},
        "updated_at": ""
    }
)

if not isinstance(currency_settings, dict):
    currency_settings = {
        "base_currency": "MYR",
        "rates": {"MYR": 1.0},
        "updated_at": ""
    }

currency_settings.setdefault("base_currency", "MYR")
currency_settings.setdefault("rates", {})
if not isinstance(currency_settings["rates"], dict):
    currency_settings["rates"] = {}
currency_settings["rates"][str(currency_settings["base_currency"]).upper()] = 1.0
if not os.path.exists(CURRENCY_FILE):
    save_json(CURRENCY_FILE, currency_settings)

# Old transactions remain fully compatible. Their original currency is MYR.
_currency_changed = False
_base_currency = str(currency_settings["base_currency"]).upper()
for _t in transactions:
    if not isinstance(_t, dict):
        continue
    if "currency" not in _t:
        _t["currency"] = _base_currency
        _currency_changed = True
    else:
        _t["currency"] = str(_t["currency"]).upper()
    if "original_amount" not in _t:
        try:
            _t["original_amount"] = float(_t.get("amount", 0))
        except (ValueError, TypeError):
            _t["original_amount"] = 0.0
        _currency_changed = True
    if "exchange_rate" not in _t:
        _t["exchange_rate"] = 1.0
        _currency_changed = True
    if "base_amount" not in _t:
        try:
            _t["base_amount"] = float(_t.get("amount", 0))
        except (ValueError, TypeError):
            _t["base_amount"] = 0.0
        _currency_changed = True
    # Account migration: old transactions go to the default Cash account.
    if not str(_t.get("account", "")).strip():
        _t["account"] = "Cash"
        _currency_changed = True
    # Keep amount as the original transaction amount for backward compatibility.
    try:
        _t["amount"] = float(_t.get("original_amount", _t.get("amount", 0)))
    except (ValueError, TypeError):
        _t["amount"] = 0.0

if _currency_changed:
    save_json(TRANSACTION_FILE, transactions)


def get_original_amount(item):
    try:
        return float(item.get("original_amount", item.get("amount", 0)))
    except (ValueError, TypeError):
        return 0.0


def get_base_amount(item):
    try:
        return float(item.get("base_amount", item.get("amount", 0)))
    except (ValueError, TypeError):
        return 0.0


def get_currency(item):
    return str(item.get("currency", _base_currency)).upper()


def get_amount(item):
    # Reports, dashboard, budgets and analytics use the base-currency amount.
    return get_base_amount(item)
