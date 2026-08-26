# ==========================================================
# MONEY TRACKER - ACCOUNTS / WALLETS MODULE
# ==========================================================
from common import *

ACCOUNT_FILE = os.path.join(DATA_FOLDER, "accounts.json")

DEFAULT_ACCOUNT_NAME = "Cash"

accounts = load_json(ACCOUNT_FILE, [])

if not isinstance(accounts, list):
    accounts = []


def save_accounts():
    save_json(ACCOUNT_FILE, accounts)


def _clean_name(name):
    return str(name).strip()


def ensure_accounts():
    """Create the default Cash account and migrate old transactions."""
    changed = False

    cleaned = []
    seen = set()
    for account in accounts:
        if not isinstance(account, dict):
            continue
        name = _clean_name(account.get("name", ""))
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        account.setdefault("type", "Cash")
        account.setdefault("currency", get_base_currency_safe())
        account["currency"] = str(account.get("currency", get_base_currency_safe())).upper()
        account.setdefault("active", True)
        cleaned.append(account)

    accounts[:] = cleaned

    if not accounts:
        accounts.append({
            "name": DEFAULT_ACCOUNT_NAME,
            "type": "Cash",
            "currency": get_base_currency_safe(),
            "active": True
        })
        changed = True

    default_name = accounts[0]["name"]

    for t in transactions:
        if not isinstance(t, dict):
            continue
        if not str(t.get("account", "")).strip():
            t["account"] = default_name
            changed = True

    if changed:
        save_accounts()
        save_json(TRANSACTION_FILE, transactions)


def get_base_currency_safe():
    return str(
        currency_settings.get("base_currency", "MYR")
    ).upper()


def get_active_accounts():
    return [
        a for a in accounts
        if isinstance(a, dict) and a.get("active", True)
    ]


def get_account_names():
    return [a.get("name", "") for a in get_active_accounts()]


def find_account(name):
    wanted = _clean_name(name).casefold()
    for account in accounts:
        if str(account.get("name", "")).casefold() == wanted:
            return account
    return None


def choose_account():
    ensure_accounts()
    active = get_active_accounts()

    print("\n========== SELECT ACCOUNT ==========")
    for i, account in enumerate(active, 1):
        print(
            f"{i}. {account.get('name')} "
            f"[{account.get('type', 'Other')}] "
            f"({account.get('currency', get_base_currency_safe())})"
        )

    while True:
        try:
            choice = int(input("Choose account: ").strip())
            if 1 <= choice <= len(active):
                return active[choice - 1]["name"]
        except ValueError:
            pass
        print("Invalid account choice.")


def add_account():
    ensure_accounts()
    print("\n========== ADD ACCOUNT ==========")

    while True:
        name = _clean_name(input("Account name: "))
        if not name:
            print("Account name cannot be empty.")
            continue
        if find_account(name):
            print("An account with this name already exists.")
            continue
        break

    account_types = ["Cash", "Bank", "eWallet", "Card", "Other"]
    print("\nAccount type:")
    for i, item in enumerate(account_types, 1):
        print(f"{i}. {item}")

    while True:
        try:
            choice = int(input("Choose type: ").strip())
            if 1 <= choice <= len(account_types):
                account_type = account_types[choice - 1]
                break
        except ValueError:
            pass
        print("Invalid choice.")

    currency = input(
        f"Account currency [Enter = {get_base_currency_safe()}]: "
    ).strip().upper()
    if not currency:
        currency = get_base_currency_safe()

    accounts.append({
        "name": name,
        "type": account_type,
        "currency": currency,
        "active": True
    })
    save_accounts()

    print(f"Account '{name}' created successfully.")


def show_accounts():
    ensure_accounts()
    print("\n========== ACCOUNTS ==========")

    for account in accounts:
        name = account.get("name", "Unknown")
        account_currency = str(account.get("currency", get_base_currency_safe())).upper()
        balance_base = 0.0

        for t in transactions:
            if str(t.get("account", "Cash")).casefold() != name.casefold():
                continue
            amount = get_base_amount(t)
            if t.get("type") == "Income":
                balance_base += amount
            elif t.get("type") == "Expense":
                balance_base -= amount

        try:
            if account_currency == get_base_currency_safe():
                local_balance = balance_base
            else:
                # Account balance is stored/calculated in base currency.
                # Convert base -> account currency for display.
                from currency import convert_from_base
                local_balance = convert_from_base(balance_base, account_currency)
        except Exception:
            local_balance = balance_base

        status = "Active" if account.get("active", True) else "Inactive"
        print("\n------------------------------------------")
        print(f"Account  : {name}")
        print(f"Type     : {account.get('type', 'Other')}")
        print(f"Currency : {account_currency}")
        print(f"Balance  : {local_balance:.2f} {account_currency}")
        if account_currency != get_base_currency_safe():
            print(f"Base     : {balance_base:.2f} {get_base_currency_safe()}")
        print(f"Status   : {status}")


def account_balance_base(name):
    balance = 0.0
    for t in transactions:
        if str(t.get("account", "Cash")).casefold() != str(name).casefold():
            continue
        amount = get_base_amount(t)
        if t.get("type") == "Income":
            balance += amount
        elif t.get("type") == "Expense":
            balance -= amount
    return balance


def edit_account():
    ensure_accounts()
    show_accounts()
    name = input("Enter account name to edit: ").strip()
    account = find_account(name)
    if not account:
        print("Account not found.")
        return

    new_name = input(f"Name [{account.get('name')}]: ").strip()
    if new_name:
        existing = find_account(new_name)
        if existing and existing is not account:
            print("Another account already has this name.")
            return
        old_name = account["name"]
        account["name"] = new_name
        for t in transactions:
            if str(t.get("account", "")).casefold() == old_name.casefold():
                t["account"] = new_name
        save_json(TRANSACTION_FILE, transactions)

    new_currency = input(
        f"Currency [{account.get('currency', get_base_currency_safe())}]: "
    ).strip().upper()
    if new_currency:
        account["currency"] = new_currency

    save_accounts()
    print("Account updated successfully.")


def delete_account():
    ensure_accounts()
    show_accounts()
    name = input("Enter account name to deactivate: ").strip()
    account = find_account(name)
    if not account:
        print("Account not found.")
        return

    if len(get_active_accounts()) <= 1:
        print("At least one active account must remain.")
        return

    if any(
        str(t.get("account", "Cash")).casefold() == name.casefold()
        for t in transactions
    ):
        print("This account has transactions and cannot be deleted.")
        print("You can edit it or keep it inactive only after moving transactions.")
        return

    account["active"] = False
    save_accounts()
    print(f"Account '{name}' deactivated.")


def delete_account_permanently():
    """Permanently remove an account when it has no transactions."""
    ensure_accounts()
    show_accounts()

    name = input("Enter account name to permanently delete: ").strip()
    account = find_account(name)

    if not account:
        print("Account not found.")
        return

    active_accounts = get_active_accounts()
    if len(active_accounts) <= 1 and account.get("active", True):
        print("At least one active account must remain.")
        return

    # Never silently remove transaction history.
    linked_transactions = [
        t for t in transactions
        if str(t.get("account", "Cash")).casefold() == name.casefold()
    ]

    if linked_transactions:
        print("This account cannot be permanently deleted because it has transactions.")
        print("Move/edit those transactions to another account first, then delete this account.")
        return

    confirm = input(
        f"Type DELETE to permanently remove account '{account.get('name')}'"
        " (this cannot be undone): "
    ).strip()

    if confirm != "DELETE":
        print("Deletion cancelled.")
        return

    accounts.remove(account)
    save_accounts()
    print(f"Account '{name}' permanently deleted.")


def account_menu():
    ensure_accounts()
    while True:
        print("\n==========================================")
        print("             ACCOUNTS / WALLETS")
        print("==========================================")
        print("1. Show Accounts")
        print("2. Add Account")
        print("3. Edit Account")
        print("4. Deactivate Account")
        print("5. Delete Account Permanently")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_accounts()
        elif choice == "2":
            add_account()
        elif choice == "3":
            edit_account()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            delete_account_permanently()
        elif choice == "6":
            return
        else:
            print("Invalid option. Please choose 1-6.")


ensure_accounts()
