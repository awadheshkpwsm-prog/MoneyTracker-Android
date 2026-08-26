# ==========================================================
# MONEY TRACKER - MULTI CURRENCY MODULE
# ==========================================================
from common import *
import json
import urllib.request
import urllib.error

CURRENCY_NAMES = {
    "MYR": ("Malaysian Ringgit", "RM", "🇲🇾"),
    "USD": ("US Dollar", "$", "🇺🇸"),
    "EUR": ("Euro", "€", "🇪🇺"),
    "GBP": ("British Pound", "£", "🇬🇧"),
    "SGD": ("Singapore Dollar", "S$", "🇸🇬"),
    "INR": ("Indian Rupee", "₹", "🇮🇳"),
    "NPR": ("Nepalese Rupee", "रू", "🇳🇵"),
    "IDR": ("Indonesian Rupiah", "Rp", "🇮🇩"),
    "THB": ("Thai Baht", "฿", "🇹🇭"),
    "AED": ("UAE Dirham", "د.إ", "🇦🇪"),
    "AUD": ("Australian Dollar", "A$", "🇦🇺"),
    "CAD": ("Canadian Dollar", "C$", "🇨🇦"),
    "JPY": ("Japanese Yen", "¥", "🇯🇵"),
    "CNY": ("Chinese Yuan", "¥", "🇨🇳"),
    "KRW": ("South Korean Won", "₩", "🇰🇷"),
    "HKD": ("Hong Kong Dollar", "HK$", "🇭🇰"),
    "NZD": ("New Zealand Dollar", "NZ$", "🇳🇿"),
    "CHF": ("Swiss Franc", "CHF", "🇨🇭"),
    "BDT": ("Bangladeshi Taka", "৳", "🇧🇩"),
    "PKR": ("Pakistani Rupee", "₨", "🇵🇰"),
}


def currency_info(code):
    code = str(code).upper().strip()
    return CURRENCY_NAMES.get(
        code,
        (code, code, "💱")
    )


def get_base_currency():
    return str(
        currency_settings.get(
            "base_currency",
            "MYR"
        )
    ).upper()


def get_rates():
    rates = currency_settings.get("rates", {})
    if not isinstance(rates, dict):
        rates = {}
        currency_settings["rates"] = rates
    base = get_base_currency()
    rates[base] = 1.0
    return rates


def save_currency_settings():
    currency_settings["updated_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    save_json(CURRENCY_FILE, currency_settings)


def get_rate(currency):
    currency = str(currency).upper().strip()
    if currency == get_base_currency():
        return 1.0
    try:
        return float(get_rates().get(currency, 0))
    except (ValueError, TypeError):
        return 0.0


def convert_to_base(amount, currency, rate=None):
    amount = float(amount)
    currency = str(currency).upper().strip()
    if currency == get_base_currency():
        return round(amount, 2), 1.0
    if rate is None:
        rate = get_rate(currency)
    rate = float(rate)
    if rate <= 0:
        raise ValueError(
            f"Exchange rate for {currency} is not configured."
        )
    # Stored rate means: 1 BASE = RATE FOREIGN.
    # Therefore FOREIGN -> BASE is division.
    return round(amount / rate, 2), rate

def convert_from_base(amount, currency):
    amount = float(amount)
    currency = str(currency).upper().strip()
    if currency == get_base_currency():
        return round(amount, 2)
    rate = get_rate(currency)
    if rate <= 0:
        raise ValueError(
            f"Exchange rate for {currency} is not configured."
        )
    # Stored rate means: 1 BASE = RATE FOREIGN.
    # Therefore BASE -> FOREIGN is multiplication.
    return round(amount * rate, 2)

def choose_currency(prompt="Choose currency"):
    codes = list(CURRENCY_NAMES.keys())
    print("\n========== CURRENCY ==========")
    for i, code in enumerate(codes, 1):
        name, symbol, flag = currency_info(code)
        rate = get_rate(code)
        rate_text = "configured" if code == get_base_currency() or rate > 0 else "rate not set"
        print(f"{i}. {flag} {code} - {name} ({symbol}) [{rate_text}]")
    print(f"Base currency: {get_base_currency()}")
    while True:
        choice = input(f"{prompt} [1-{len(codes)}]: ").strip()
        try:
            number = int(choice)
            if 1 <= number <= len(codes):
                return codes[number - 1]
        except ValueError:
            pass
        print("Invalid currency choice.")


def ensure_currency_rate(currency):
    currency = str(currency).upper().strip()
    if currency == get_base_currency():
        return 1.0
    rate = get_rate(currency)
    if rate > 0:
        return rate
    print(
        f"Exchange rate for {currency} is not configured."
    )
    print(
        f"Enter how many {currency} equal 1 {get_base_currency()}."
    )
    while True:
        try:
            value = float(input("Exchange rate: ").strip())
            if value <= 0:
                print("Rate must be greater than zero.")
                continue
            get_rates()[currency] = value
            save_currency_settings()
            return value
        except ValueError:
            print("Invalid exchange rate.")


def update_rates_from_internet():
    base = get_base_currency()
    url = f"https://open.er-api.com/v6/latest/{base}"
    print(f"\nFetching live rates for {base}...")
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "MoneyTracker/1.0"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        rates = data.get("rates", {})
        if not isinstance(rates, dict):
            raise ValueError("Invalid rate data received.")
        stored = get_rates()
        updated = 0
        for code in CURRENCY_NAMES:
            if code in rates:
                try:
                    stored[code] = float(rates[code])
                    updated += 1
                except (ValueError, TypeError):
                    pass
        stored[base] = 1.0
        save_currency_settings()
        print(f"Live rates updated successfully: {updated} currencies.")
        return True
    except Exception as error:
        print("Could not update live rates.")
        print(f"Reason: {error}")
        print("You can still enter rates manually.")
        return False


def set_exchange_rate():
    print("\n========== SET EXCHANGE RATE ==========")
    currency = choose_currency("Choose currency")
    base = get_base_currency()
    if currency == base:
        print(f"{base} is the base currency. Its rate is always 1.000000.")
        return
    while True:
        try:
            rate = float(
                input(
                    f"1 {base} = how many {currency}? Current [{get_rate(currency) or 'not set'}]: "
                ).strip()
            )
            if rate <= 0:
                print("Rate must be greater than zero.")
                continue
            get_rates()[currency] = rate
            save_currency_settings()
            print("Exchange rate saved successfully.")
            break
        except ValueError:
            print("Invalid exchange rate.")


def show_exchange_rates():
    print("\n========== EXCHANGE RATES ==========")
    base = get_base_currency()
    print(f"Base currency: {base}")
    print(f"Last update: {currency_settings.get('updated_at', 'Never')}")
    print(f"\n1 unit of {base} = foreign currency")
    for code in CURRENCY_NAMES:
        name, symbol, flag = currency_info(code)
        rate = get_rate(code)
        status = f"{rate:.8f}" if rate > 0 else "NOT SET"
        print(f"{flag} {code:4} {symbol:>4}  {status:>12}  {name}")


def currency_converter():
    print("\n========== CURRENCY CONVERTER ==========")
    from_code = choose_currency("From currency")
    to_code = choose_currency("To currency")
    try:
        amount = float(input(f"Amount in {from_code}: ").strip())
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        base_amount, from_rate = convert_to_base(amount, from_code)
        result = convert_from_base(base_amount, to_code)
        from_name, from_symbol, _ = currency_info(from_code)
        to_name, to_symbol, _ = currency_info(to_code)
        print("\n------------------------------------------")
        print(f"{amount:.2f} {from_code} = {result:.2f} {to_code}")
        print(f"From: {from_name} ({from_symbol})")
        print(f"To  : {to_name} ({to_symbol})")
        print(f"Base equivalent: {base_amount:.2f} {get_base_currency()}")
        print("------------------------------------------")
    except (ValueError, TypeError) as error:
        print(f"Conversion failed: {error}")


def currency_summary():
    print("\n========== MULTI-CURRENCY SUMMARY ==========")
    if not transactions:
        print("No transactions available.")
        return
    base = get_base_currency()
    summary = {}
    for t in transactions:
        code = str(t.get("currency", base)).upper()
        amount = get_original_amount(t)
        if t.get("type") == "Expense":
            income_expense = -amount
        else:
            income_expense = amount
        summary.setdefault(code, {"income": 0.0, "expense": 0.0, "count": 0})
        summary[code]["count"] += 1
        if t.get("type") == "Income":
            summary[code]["income"] += amount
        else:
            summary[code]["expense"] += amount
    for code in sorted(summary):
        item = summary[code]
        base_income = sum(
            get_base_amount(t) for t in transactions
            if str(t.get("currency", base)).upper() == code and t.get("type") == "Income"
        )
        base_expense = sum(
            get_base_amount(t) for t in transactions
            if str(t.get("currency", base)).upper() == code and t.get("type") == "Expense"
        )
        print("\n------------------------------------------")
        print(f"Currency     : {code}")
        print(f"Transactions : {item['count']}")
        print(f"Income       : {item['income']:.2f} {code}")
        print(f"Expense      : {item['expense']:.2f} {code}")
        print(f"Net          : {item['income'] - item['expense']:.2f} {code}")
        print(f"Base income  : {base_income:.2f} {base}")
        print(f"Base expense : {base_expense:.2f} {base}")
        print(f"Base net     : {base_income - base_expense:.2f} {base}")


def set_base_currency():
    current = get_base_currency()
    if transactions:
        print("\nBase currency cannot be changed after transactions exist.")
        print(f"Current base currency: {current}")
        print("This protects existing converted amounts from becoming incorrect.")
        return
    new_base = choose_currency("Choose new base currency")
    currency_settings["base_currency"] = new_base
    currency_settings.setdefault("rates", {})
    currency_settings["rates"][new_base] = 1.0
    save_currency_settings()
    print(f"Base currency changed to {new_base}.")


def currency_menu():
    while True:
        print("\n==========================================")
        print("           MULTI-CURRENCY")
        print("==========================================")
        print(f"Base Currency: {get_base_currency()}")
        print("1. View Exchange Rates")
        print("2. Update Live Exchange Rates")
        print("3. Set / Update Exchange Rate")
        print("4. Currency Converter")
        print("5. Currency-wise Transaction Summary")
        print("6. Change Base Currency")
        print("7. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_exchange_rates()
        elif choice == "2":
            update_rates_from_internet()
        elif choice == "3":
            set_exchange_rate()
        elif choice == "4":
            currency_converter()
        elif choice == "5":
            currency_summary()
        elif choice == "6":
            set_base_currency()
        elif choice == "7":
            return
        else:
            print("Invalid option. Please choose 1-7.")
