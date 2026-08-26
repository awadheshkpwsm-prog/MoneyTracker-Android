# ==========================================================
# MONEY TRACKER - TRANSACTIONS MODULE
# ==========================================================
from common import *
from currency import *
from accounts import *

def get_amount(item):

    try:

        return float(
            item.get("base_amount", item.get("amount", 0))
        )

    except (ValueError, TypeError):

        return 0.0


def generate_transaction_id():

    highest_number = 0

    for t in transactions:

        transaction_id = str(
            t.get("id", "")
        )

        if transaction_id.startswith("TXN-"):

            try:

                number = int(
                    transaction_id.replace(
                        "TXN-",
                        ""
                    )
                )

                if number > highest_number:

                    highest_number = number

            except ValueError:

                pass

    return f"TXN-{highest_number + 1:04d}"

def save_transactions():

    save_json(
        FILE_NAME,
        transactions
    )

def get_valid_date():

    while True:

        date_input = input(
            "Enter date (DD-MM-YYYY) "
            "or press Enter for today: "
        ).strip()

        if not date_input:

            return datetime.now().strftime(
                "%d-%m-%Y"
            )

        try:

            valid_date = datetime.strptime(
                date_input,
                "%d-%m-%Y"
            )

            return valid_date.strftime(
                "%d-%m-%Y"
            )

        except ValueError:

            print("Invalid date.")

            print(
                "Please use DD-MM-YYYY format."
            )

def parse_date(date_text):

    try:

        return datetime.strptime(
            str(date_text),
            "%d-%m-%Y"
        )

    except ValueError:

        return None

def select_category(transaction_type):

    if transaction_type == "Expense":

        categories = EXPENSE_CATEGORIES

    else:

        categories = INCOME_CATEGORIES

    print(
        "\n========== CATEGORY =========="
    )

    for number, category in enumerate(
        categories,
        1
    ):

        print(
            f"{number}. {category}"
        )

    while True:

        try:

            choice = int(
                input(
                    "Choose category: "
                ).strip()
            )

            if 1 <= choice <= len(categories):

                return categories[
                    choice - 1
                ]

            print(
                "Please choose a valid "
                "category number."
            )

        except ValueError:

            print(
                "Please enter a number."
            )

def add_transaction():

    print(
        "\n========== ADD TRANSACTION =========="
    )

    print("1. Expense")
    print("2. Income")

    while True:

        choice = input("Choose type: ").strip()

        if choice == "1":
            transaction_type = "Expense"
            break
        elif choice == "2":
            transaction_type = "Income"
            break
        else:
            print("Please choose 1 or 2.")

    # The transaction currency is determined by the selected account.
    # This prevents an INR account from accidentally receiving a MYR transaction.
    account = choose_account()
    account_obj = find_account(account)
    if not account_obj:
        print("Selected account could not be found.")
        return

    currency = str(
        account_obj.get("currency", get_base_currency())
    ).upper().strip() or get_base_currency()

    # Base-currency accounts need no exchange rate. For foreign-currency
    # accounts, the rate must exist before the transaction can be saved.
    try:
        exchange_rate = ensure_currency_rate(currency)
    except (ValueError, TypeError) as error:
        print(f"Currency conversion failed: {error}")
        return

    print(f"Transaction currency: {currency}")
    if currency != get_base_currency():
        print(
            f"Exchange rate: 1 {get_base_currency()} = "
            f"{exchange_rate:.8f} {currency}"
        )

    try:
        amount = float(input(f"Enter amount ({currency}): ").strip())
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        base_amount, exchange_rate = convert_to_base(
            amount,
            currency,
            exchange_rate
        )
    except (ValueError, TypeError) as error:
        print(f"Invalid amount/currency conversion: {error}")
        return

    category = select_category(transaction_type)

    description = input(
        "Enter description: "
    ).strip()

    print("\nDate Entry")
    date = get_valid_date()
    transaction_id = generate_transaction_id()

    transactions.append(
        {
            "id": transaction_id,
            "date": date,
            "type": transaction_type,
            "category": category,
            "amount": amount,
            "original_amount": amount,
            "currency": currency,
            "exchange_rate": exchange_rate,
            "base_amount": base_amount,
            "base_currency": get_base_currency(),
            "account": account,
            "description": description
        }
    )

    save_transactions()

    print("\nTransaction saved successfully!")
    print(f"Transaction ID : {transaction_id}")
    print(f"Account        : {account}")
    print(f"Original Amount: {amount:.2f} {currency}")
    print(f"Exchange Rate  : 1 {get_base_currency()} = {exchange_rate:.8f} {currency}")
    print(f"Base Amount    : {base_amount:.2f} {get_base_currency()}")

def show_transactions():

    print("\n========== TRANSACTIONS ==========")

    if not transactions:
        print("No transactions yet.")
        return

    base = get_base_currency()

    for number, t in enumerate(transactions, 1):
        currency = get_currency(t)
        original = get_original_amount(t)
        base_amount = get_base_amount(t)
        rate = float(t.get("exchange_rate", 1) or 1)

        print("\n------------------------------------------")
        print(f"No.           : {number}")
        print(f"Transaction ID: {t.get('id', 'Unknown')}")
        print(f"Date          : {t.get('date', 'Unknown')}")
        print(f"Type          : {t.get('type', 'Unknown')}")
        print(f"Category      : {t.get('category', 'Uncategorized')}")
        print(f"Account       : {t.get('account', 'Cash')}")
        print(f"Amount        : {original:.2f} {currency}")
        if currency != base:
            print(f"Exchange Rate : 1 {base} = {rate:.8f} {currency}")
            print(f"Base Amount   : {base_amount:.2f} {base}")
        print(f"Description   : {t.get('description', '')}")

    print("\n------------------------------------------")
    print(f"Total Transactions: {len(transactions)}")

def search_transactions():

    print(
        "\n========== SEARCH & FILTER =========="
    )

    if not transactions:

        print("No transactions yet.")

        return

    keyword = input(
        "Enter ID, date, category, "
        "type or description: "
    ).strip().lower()

    if not keyword:

        print("Search cancelled.")

        return

    results = []

    for t in transactions:

        values = [

            str(
                t.get("id", "")
            ),

            str(
                t.get("type", "")
            ),

            str(
                t.get("category", "")
            ),

            str(
                t.get("description", "")
            ),

            str(
                t.get("date", "")
            )
        ]

        if any(
            keyword in value.lower()
            for value in values
        ):

            results.append(t)

    print(
        "\n========== SEARCH RESULTS =========="
    )

    if not results:

        print(
            "No matching transactions found."
        )

        return

    for number, t in enumerate(
        results,
        1
    ):

        print(
            "\n------------------------------------------"
        )

        print(
            f"{number}. "
            f"{t.get('id', 'Unknown')} | "
            f"{t.get('date', 'Unknown')} | "
            f"{t.get('type', 'Unknown')} | "
            f"{t.get('category', 'Uncategorized')} | "
            f"RM {get_amount(t):.2f} | "
            f"{t.get('description', '')}"
        )

    print(
        "------------------------------------------"
    )

    print(
        f"Matching Transactions: "
        f"{len(results)}"
    )

    print(
        "\n1. Export Search Results to PDF"
    )

    print("2. Back")

    choice = input(
        "Choose option: "
    ).strip()

    if choice == "1":

        export_transactions_to_pdf(
            results,
            "Search Transaction Report"
        )

def find_transaction():

    if not transactions:

        print(
            "No transactions available."
        )

        return None

    search_id = input(
        "Enter Transaction ID: "
    ).strip().upper()

    for index, t in enumerate(
        transactions
    ):

        if str(
            t.get("id", "")
        ).upper() == search_id:

            return index

    print(
        "Transaction ID not found."
    )

    return None

def display_filtered_transactions(
    results
):

    if not results:

        print(
            "\nNo transactions found."
        )

        return

    total_income = 0

    total_expense = 0

    print(
        "\n========== FILTERED TRANSACTIONS =========="
    )

    for number, t in enumerate(
        results,
        1
    ):

        amount = get_amount(t)

        if t.get("type") == "Income":

            total_income += amount

        elif t.get("type") == "Expense":

            total_expense += amount

        print(
            "\n------------------------------------------"
        )

        print(
            f"No.           : {number}"
        )

        print(
            f"ID            : "
            f"{t.get('id', 'Unknown')}"
        )

        print(
            f"Date          : "
            f"{t.get('date', '')}"
        )

        print(
            f"Type          : "
            f"{t.get('type', '')}"
        )

        print(
            f"Category      : "
            f"{t.get('category', '')}"
        )

        print(
            f"Amount        : RM {amount:.2f}"
        )

        print(
            f"Description   : "
            f"{t.get('description', '')}"
        )

    print(
        "\n=========================================="
    )

    print(
        f"Filtered Transactions : "
        f"{len(results)}"
    )

    print(
        f"Filtered Income       : "
        f"RM {total_income:.2f}"
    )

    print(
        f"Filtered Expense      : "
        f"RM {total_expense:.2f}"
    )

    print(
        f"Filtered Balance      : "
        f"RM {total_income - total_expense:.2f}"
    )

    print(
        "=========================================="
    )

def advanced_transaction_filter():

    print(
        "\n=========================================="
    )

    print(
        "       ADVANCED TRANSACTION FILTER"
    )

    print(
        "=========================================="
    )

    if not transactions:

        print(
            "No transactions available."
        )

        return

    print(
        "\nLeave any field empty "
        "to ignore that filter."
    )

    keyword = input(
        "\nSearch ID / description / "
        "category / date: "
    ).strip().lower()

    print(
        "\nTransaction Type:"
    )

    print("1. All")

    print("2. Income")

    print("3. Expense")

    type_choice = input(
        "Choose type [1]: "
    ).strip()

    if type_choice == "2":

        selected_type = "Income"

    elif type_choice == "3":

        selected_type = "Expense"

    else:

        selected_type = ""

    print(
        "\nCategory filter:"
    )

    print(
        "Enter category name "
        "or press Enter for all."
    )

    category_filter = input(
        "Category: "
    ).strip().lower()

    min_amount = None

    min_input = input(
        "\nMinimum amount "
        "[Enter = no minimum]: RM "
    ).strip()

    if min_input:

        try:

            min_amount = float(
                min_input
            )

            if min_amount < 0:

                print(
                    "Minimum amount "
                    "cannot be negative."
                )

                return

        except ValueError:

            print(
                "Invalid minimum amount."
            )

            return

    max_amount = None

    max_input = input(
        "Maximum amount "
        "[Enter = no maximum]: RM "
    ).strip()

    if max_input:

        try:

            max_amount = float(
                max_input
            )

            if max_amount < 0:

                print(
                    "Maximum amount "
                    "cannot be negative."
                )

                return

        except ValueError:

            print(
                "Invalid maximum amount."
            )

            return

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):

        print(
            "Minimum amount cannot be "
            "greater than maximum amount."
        )

        return

    print("\nDate Range:")

    print(
        "Use DD-MM-YYYY format."
    )

    start_date_text = input(
        "Start date "
        "[Enter = no start date]: "
    ).strip()

    end_date_text = input(
        "End date "
        "[Enter = no end date]: "
    ).strip()

    start_date = None

    end_date = None

    if start_date_text:

        start_date = parse_date(
            start_date_text
        )

        if start_date is None:

            print(
                "Invalid start date."
            )

            return

    if end_date_text:

        end_date = parse_date(
            end_date_text
        )

        if end_date is None:

            print(
                "Invalid end date."
            )

            return

    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):

        print(
            "Start date cannot be "
            "after end date."
        )

        return

    results = []

    for t in transactions:

        transaction_type = str(
            t.get("type", "")
        )

        category = str(
            t.get("category", "")
        )

        description = str(
            t.get("description", "")
        )

        transaction_id = str(
            t.get("id", "")
        )

        date_text = str(
            t.get("date", "")
        )

        amount = get_amount(t)

        if keyword:

            searchable_text = (
                transaction_id
                + " "
                + transaction_type
                + " "
                + category
                + " "
                + description
                + " "
                + date_text
            ).lower()

            if keyword not in searchable_text:

                continue

        if selected_type:

            if transaction_type != selected_type:

                continue

        if category_filter:

            if (
                category_filter
                not in category.lower()
            ):

                continue

        if (
            min_amount is not None
            and amount < min_amount
        ):

            continue

        if (
            max_amount is not None
            and amount > max_amount
        ):

            continue

        transaction_date = parse_date(
            date_text
        )

        if start_date is not None:

            if transaction_date is None:

                continue

            if transaction_date < start_date:

                continue

        if end_date is not None:

            if transaction_date is None:

                continue

            if transaction_date > end_date:

                continue

        results.append(t)

    display_filtered_transactions(
        results
    )

    if results:

        print(
            "\n1. Export filtered results to PDF"
        )

        print("2. Back")

        export_choice = input(
            "Choose option: "
        ).strip()

        if export_choice == "1":

            export_transactions_to_pdf(
                results,
                "Filtered Transactions Report"
            )

def sort_transactions():

    print(
        "\n=========================================="
    )

    print(
        "          TRANSACTION SORTING"
    )

    print(
        "=========================================="
    )

    if not transactions:

        print(
            "No transactions available."
        )

        return

    print(
        "\n1. Newest Date First"
    )

    print(
        "2. Oldest Date First"
    )

    print(
        "3. Highest Amount First"
    )

    print(
        "4. Lowest Amount First"
    )

    print(
        "5. Income First"
    )

    print(
        "6. Expense First"
    )

    print(
        "7. Category A-Z"
    )

    print(
        "8. Transaction ID A-Z"
    )

    print(
        "9. Back"
    )

    choice = input(
        "\nChoose sorting option: "
    ).strip()

    sorted_transactions = list(
        transactions
    )

    if choice == "1":

        sorted_transactions.sort(
            key=lambda t: (
                parse_date(
                    t.get("date", "")
                )
                or datetime.min
            ),
            reverse=True
        )

    elif choice == "2":

        sorted_transactions.sort(
            key=lambda t: (
                parse_date(
                    t.get("date", "")
                )
                or datetime.min
            )
        )

    elif choice == "3":

        sorted_transactions.sort(
            key=get_amount,
            reverse=True
        )

    elif choice == "4":

        sorted_transactions.sort(
            key=get_amount
        )

    elif choice == "5":

        sorted_transactions.sort(
            key=lambda t: (
                0
                if t.get("type") == "Income"
                else 1
            )
        )

    elif choice == "6":

        sorted_transactions.sort(
            key=lambda t: (
                0
                if t.get("type") == "Expense"
                else 1
            )
        )

    elif choice == "7":

        sorted_transactions.sort(
            key=lambda t: str(
                t.get(
                    "category",
                    ""
                )
            ).lower()
        )

    elif choice == "8":

        sorted_transactions.sort(
            key=lambda t: str(
                t.get(
                    "id",
                    ""
                )
            ).lower()
        )

    elif choice == "9":

        return

    else:

        print(
            "Invalid option."
        )

        return

    display_filtered_transactions(
        sorted_transactions
    )

    print(
        "\n1. Export Sorted Results to PDF"
    )

    print("2. Back")

    export_choice = input(
        "Choose option: "
    ).strip()

    if export_choice == "1":

        export_transactions_to_pdf(
            sorted_transactions,
            "Sorted Transaction Report"
        )

def quick_date_filter():

    print(
        "\n=========================================="
    )

    print(
        "             QUICK DATE FILTER"
    )

    print(
        "=========================================="
    )

    if not transactions:

        print(
            "No transactions available."
        )

        return

    print(
        "\n1. Today"
    )

    print(
        "2. This Week"
    )

    print(
        "3. This Month"
    )

    print(
        "4. This Year"
    )

    print(
        "5. Custom Date Range"
    )

    print(
        "6. Back"
    )

    choice = input(
        "\nChoose option: "
    ).strip()

    if choice == "6":

        return

    today = datetime.now()

    start_date = None

    end_date = today

    if choice == "1":

        start_date = today.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end_date = today

    elif choice == "2":

        weekday = today.weekday()

        start_date = today.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        start_date = (
            start_date
            - __import__(
                "datetime"
            ).timedelta(
                days=weekday
            )
        )

    elif choice == "3":

        start_date = today.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    elif choice == "4":

        start_date = today.replace(
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    elif choice == "5":

        start_text = input(
            "Start date (DD-MM-YYYY): "
        ).strip()

        end_text = input(
            "End date (DD-MM-YYYY): "
        ).strip()

        start_date = parse_date(
            start_text
        )

        end_date = parse_date(
            end_text
        )

        if (
            start_date is None
            or end_date is None
        ):

            print(
                "Invalid date."
            )

            return

        if start_date > end_date:

            print(
                "Start date cannot be "
                "after end date."
            )

            return

    else:

        print(
            "Invalid option."
        )

        return

    results = []

    for t in transactions:

        transaction_date = parse_date(
            t.get("date", "")
        )

        if transaction_date is None:

            continue

        if (
            transaction_date >= start_date
            and transaction_date <= end_date
        ):

            results.append(t)

    display_filtered_transactions(
        results
    )

    if results:

        print(
            "\n1. Export Quick Filter PDF"
        )

        print("2. Back")

        export_choice = input(
            "Choose option: "
        ).strip()

        if export_choice == "1":

            filter_names = {
                "1": "Today",
                "2": "This Week",
                "3": "This Month",
                "4": "This Year",
                "5": "Custom Date Range"
            }

            title = (
                "Quick Filter - "
                + filter_names.get(
                    choice,
                    "Transactions"
                )
            )

            export_transactions_to_pdf(
                results,
                title
            )

def combined_transaction_filter():

    print(
        "\n=========================================="
    )

    print(
        "       COMBINED TRANSACTION FILTER"
    )

    print(
        "=========================================="
    )

    if not transactions:

        print(
            "No transactions available."
        )

        return

    keyword = input(
        "\nKeyword "
        "[ID/category/description/date]: "
    ).strip().lower()

    print(
        "\nTransaction Type:"
    )

    print("1. All")

    print("2. Income")

    print("3. Expense")

    type_choice = input(
        "Choose type [1]: "
    ).strip()

    if type_choice == "2":

        selected_type = "Income"

    elif type_choice == "3":

        selected_type = "Expense"

    else:

        selected_type = ""

    category_filter = input(
        "Category [Enter = all]: "
    ).strip().lower()

    min_amount = None

    max_amount = None

    min_text = input(
        "Minimum amount "
        "[Enter = all]: RM "
    ).strip()

    if min_text:

        try:

            min_amount = float(
                min_text
            )

        except ValueError:

            print(
                "Invalid minimum amount."
            )

            return

    max_text = input(
        "Maximum amount "
        "[Enter = all]: RM "
    ).strip()

    if max_text:

        try:

            max_amount = float(
                max_text
            )

        except ValueError:

            print(
                "Invalid maximum amount."
            )

            return

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):

        print(
            "Minimum cannot be greater "
            "than maximum."
        )

        return

    results = []

    for t in transactions:

        transaction_id = str(
            t.get("id", "")
        )

        transaction_type = str(
            t.get("type", "")
        )

        category = str(
            t.get("category", "")
        )

        description = str(
            t.get("description", "")
        )

        date_text = str(
            t.get("date", "")
        )

        amount = get_amount(t)

        searchable = (
            transaction_id
            + " "
            + transaction_type
            + " "
            + category
            + " "
            + description
            + " "
            + date_text
        ).lower()

        if keyword:

            if keyword not in searchable:

                continue

        if selected_type:

            if transaction_type != selected_type:

                continue

        if category_filter:

            if (
                category_filter
                not in category.lower()
            ):

                continue

        if (
            min_amount is not None
            and amount < min_amount
        ):

            continue

        if (
            max_amount is not None
            and amount > max_amount
        ):

            continue

        results.append(t)

    if not results:

        print(
            "\nNo matching transactions."
        )

        return

    print(
        "\nSort Results:"
    )

    print("1. Newest First")

    print("2. Oldest First")

    print("3. Highest Amount")

    print("4. Lowest Amount")

    print("5. No Sorting")

    sort_choice = input(
        "Choose sorting [5]: "
    ).strip()

    if sort_choice == "1":

        results.sort(
            key=lambda t: (
                parse_date(
                    t.get("date", "")
                )
                or datetime.min
            ),
            reverse=True
        )

    elif sort_choice == "2":

        results.sort(
            key=lambda t: (
                parse_date(
                    t.get("date", "")
                )
                or datetime.min
            )
        )

    elif sort_choice == "3":

        results.sort(
            key=get_amount,
            reverse=True
        )

    elif sort_choice == "4":

        results.sort(
            key=get_amount
        )

    display_filtered_transactions(
        results
    )

    print(
        "\n1. Export Combined Filter PDF"
    )

    print("2. Back")

    export_choice = input(
        "Choose option: "
    ).strip()

    if export_choice == "1":

        export_transactions_to_pdf(
            results,
            "Combined Transaction Filter Report"
        )

def export_transactions_to_pdf(
    data,
    title="Transaction Report"
):

    if not data:

        print(
            "No data available for PDF export."
        )

        return

    try:

        from reportlab.lib.pagesizes import A4

        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

        from reportlab.lib import colors

        from reportlab.lib.styles import (
            getSampleStyleSheet
        )

    except ImportError:

        print(
            "\nReportLab is not installed."
        )

        print(
            "Please install it using:"
        )

        print(
            "pip install reportlab"
        )

        return

    if not os.path.exists(
        PDF_FOLDER
    ):

        os.makedirs(
            PDF_FOLDER
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"MoneyTracker_{timestamp}.pdf"
    )

    filepath = os.path.join(
        PDF_FOLDER,
        filename
    )

    try:

        document = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=25,
            leftMargin=25,
            topMargin=30,
            bottomMargin=30
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "MONEY TRACKER",
                styles["Title"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        elements.append(
            Paragraph(
                title,
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        total_income = 0

        total_expense = 0

        table_data = [
            [
                "ID",
                "Date",
                "Type",
                "Category",
                "Currency",
                "Original Amount",
                "Base Amount",
                "Description"
            ]
        ]

        for t in data:

            amount = get_amount(t)

            if t.get("type") == "Income":

                total_income += amount

            elif t.get("type") == "Expense":

                total_expense += amount

            table_data.append(
                [
                    str(
                        t.get(
                            "id",
                            ""
                        )
                    ),

                    str(
                        t.get(
                            "date",
                            ""
                        )
                    ),

                    str(
                        t.get(
                            "type",
                            ""
                        )
                    ),

                    str(
                        t.get(
                            "category",
                            ""
                        )
                    ),

                    get_currency(t),

                    f"{get_original_amount(t):.2f}",

                    f"{amount:.2f} {get_base_currency()}",

                    str(
                        t.get(
                            "description",
                            ""
                        )
                    )
                ]
            )

        table = Table(
            table_data,
            repeatRows=1
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    )
                ]
            )
        )

        elements.append(table)

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                f"Total Transactions: "
                f"{len(data)}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Total Income: "
                f"{get_base_currency()} {total_income:.2f}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Total Expense: "
                f"{get_base_currency()} {total_expense:.2f}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Balance: "
                f"{get_base_currency()} "
                f"{total_income - total_expense:.2f}",
                styles["Normal"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        elements.append(
            Paragraph(
                "Generated: "
                + datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                styles["Normal"]
            )
        )

        document.build(
            elements
        )

        print(
            "\nPDF exported successfully!"
        )

        print(
            f"File: {filepath}"
        )

    except Exception as error:

        print(
            "\nPDF export failed."
        )

        print(
            f"Error: {error}"
        )

def export_all_transactions_pdf():

    if not transactions:

        print(
            "No transactions available."
        )

        return

    export_transactions_to_pdf(
        transactions,
        "All Transactions Report"
    )

def edit_transaction():

    show_transactions()

    if not transactions:
        return

    print("\nYou can edit a transaction using:")
    print("1. Transaction Number")
    print("2. Transaction ID")
    choice = input("Choose method: ").strip()
    index = None

    try:
        if choice == "1":
            number = int(input("Enter transaction number: ").strip())
            if not (1 <= number <= len(transactions)):
                print("Invalid transaction number.")
                return
            index = number - 1
        elif choice == "2":
            index = find_transaction()
            if index is None:
                return
        else:
            print("Invalid choice.")
            return

        t = transactions[index]
        old_currency = get_currency(t)
        old_amount = get_original_amount(t)
        old_rate = float(t.get("exchange_rate", 1) or 1)

        print("\n========== EDIT TRANSACTION ==========")
        print(f"Transaction ID : {t.get('id', 'Unknown')}")
        print("\nPress Enter to keep the old value.")

        print(f"\nCurrent Type: {t.get('type', 'Expense')}")
        print("1. Expense")
        print("2. Income")
        type_input = input("Choose new type [Enter = keep old]: ").strip()
        if type_input == "1":
            transaction_type = "Expense"
        elif type_input == "2":
            transaction_type = "Income"
        elif type_input == "":
            transaction_type = t.get("type", "Expense")
        else:
            print("Invalid type.")
            return

        amount_input = input(
            f"Amount [{old_amount:.2f} {old_currency}]: "
        ).strip()
        if amount_input:
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
        else:
            amount = old_amount

        old_account = t.get("account", "Cash")
        print(f"Current Account: {old_account}")
        account_change = input("Change account? Y/N: ").strip().upper()
        if account_change == "Y":
            account = choose_account()
        else:
            account = old_account

        account_obj = find_account(account)
        if not account_obj:
            print("Account not found.")
            return

        # Edited transactions also follow the account currency.
        currency = str(
            account_obj.get("currency", get_base_currency())
        ).upper().strip() or get_base_currency()

        try:
            exchange_rate = ensure_currency_rate(currency)
        except (ValueError, TypeError) as error:
            print(f"Currency conversion failed: {error}")
            return

        # If the account currency changed, interpret the entered amount in
        # the selected account currency.
        if old_currency != currency:
            print(
                f"Account currency is {currency}. "
                f"The transaction will use {currency}."
            )

        base_amount, exchange_rate = convert_to_base(
            amount, currency, exchange_rate
        )

        current_category = t.get("category", "Uncategorized")
        print(f"\nCurrent Category: {current_category}")
        category_choice = input("Change category? Y/N: ").strip().upper()
        if category_choice == "Y":
            category = select_category(transaction_type)
        else:
            category = current_category

        description_input = input(
            f"Description [{t.get('description', '')}]: "
        ).strip()
        description = description_input if description_input else t.get("description", "")

        current_date = t.get("date", "")
        print(f"Current Date: {current_date}")
        change_date = input("Change date? Y/N: ").strip().upper()
        date = get_valid_date() if change_date == "Y" else current_date

        t["type"] = transaction_type
        t["amount"] = amount
        t["original_amount"] = amount
        t["currency"] = currency
        t["exchange_rate"] = exchange_rate
        t["base_amount"] = base_amount
        t["base_currency"] = get_base_currency()
        t["account"] = account
        t["category"] = category
        t["description"] = description
        t["date"] = date

        save_transactions()

        print("\nTransaction updated successfully!")
        print(f"Account        : {account}")
        print(f"Original Amount: {amount:.2f} {currency}")
        print(f"Base Amount    : {base_amount:.2f} {get_base_currency()}")
        print(f"Transaction ID : {t.get('id', 'Unknown')}")

    except (ValueError, TypeError) as error:
        print(f"Please enter valid values. {error}")

def delete_transaction():

    show_transactions()

    if not transactions:

        return

    print(
        "\nYou can delete using:"
    )

    print(
        "1. Transaction Number"
    )

    print(
        "2. Transaction ID"
    )

    choice = input(
        "Choose method: "
    ).strip()

    index = None

    try:

        if choice == "1":

            number = int(
                input(
                    "Enter transaction "
                    "number to delete: "
                ).strip()
            )

            if not (
                1
                <= number
                <= len(transactions)
            ):

                print(
                    "Invalid transaction number."
                )

                return

            index = number - 1

        elif choice == "2":

            index = find_transaction()

            if index is None:

                return

        else:

            print(
                "Invalid choice."
            )

            return

        transaction = transactions[index]

        print(
            "\n========== TRANSACTION TO DELETE =========="
        )

        print(
            f"ID          : "
            f"{transaction.get('id', 'Unknown')}"
        )

        print(
            f"Date        : "
            f"{transaction.get('date', '')}"
        )

        print(
            f"Type        : "
            f"{transaction.get('type', '')}"
        )

        print(
            f"Category    : "
            f"{transaction.get('category', '')}"
        )

        print(
            f"Amount      : "
            f"RM {get_amount(transaction):.2f}"
        )

        print(
            f"Description : "
            f"{transaction.get('description', '')}"
        )

        confirm = input(
            "\nAre you sure? "
            "Type YES to delete: "
        ).strip()

        if confirm.upper() == "YES":

            deleted = transactions.pop(
                index
            )

            save_transactions()

            print(
                "\nTransaction deleted successfully!"
            )

            print(
                f"Deleted ID: "
                f"{deleted.get('id', 'Unknown')}"
            )

        else:

            print(
                "Delete cancelled."
            )

    except ValueError:

        print(
            "Please enter a valid number."
        )
