# ==========================================================
# MONEY TRACKER - ANALYTICS MODULE
# ==========================================================
from common import *
from currency import *

def _dashboard_convert(base_amount, display_currency):
    if display_currency == get_base_currency():
        return float(base_amount)
    try:
        return float(convert_from_base(float(base_amount), display_currency))
    except Exception:
        return float(base_amount)


def _render_dashboard(display_currency):
    """Render dashboard values in the selected display currency."""
    base = get_base_currency()

    total_income_base = sum(
        get_amount(t)
        for t in transactions
        if t.get("type") == "Income"
    )

    total_expense_base = sum(
        get_amount(t)
        for t in transactions
        if t.get("type") == "Expense"
    )

    balance_base = total_income_base - total_expense_base
    current_month = datetime.now().strftime("%m-%Y")
    month_income_base = 0.0
    month_expense_base = 0.0
    category_expenses = {}

    for t in transactions:
        date = str(t.get("date", ""))
        if date.endswith(current_month):
            amount = get_amount(t)
            if t.get("type") == "Income":
                month_income_base += amount
            elif t.get("type") == "Expense":
                month_expense_base += amount
                category = t.get("category", "Uncategorized")
                category_expenses[category] = category_expenses.get(category, 0) + amount

    month_balance_base = month_income_base - month_expense_base

    if category_expenses:
        top_category = max(category_expenses, key=category_expenses.get)
        top_category_amount_base = category_expenses[top_category]
    else:
        top_category = "None"
        top_category_amount_base = 0.0

    monthly_budget_base = float(budgets.get(current_month, 0))
    budget_remaining_base = monthly_budget_base - month_expense_base
    budget_used = (month_expense_base / monthly_budget_base * 100) if monthly_budget_base > 0 else 0

    total_lent = sum(
        float(loan.get("remaining", 0))
        for loan in loans
        if loan.get("type") == "Lending"
    )
    total_borrowed = sum(
        float(loan.get("remaining", 0))
        for loan in loans
        if loan.get("type") == "Borrowing"
    )

    def money(value):
        return f"{_dashboard_convert(value, display_currency):.2f} {display_currency}"

    print("\n==========================================")
    print("             MONEY TRACKER")
    print("            SMART DASHBOARD")
    print("==========================================")
    print(f"Display Currency   : {display_currency}")
    print(f"Base Currency      : {base}")
    print("------------------------------------------")
    print(f"Total Income       : {money(total_income_base)}")
    print(f"Total Expense      : {money(total_expense_base)}")
    print(f"Balance            : {money(balance_base)}")
    print(f"Transactions       : {len(transactions)}")
    print("------------------------------------------")
    print(f"THIS MONTH ({current_month})")
    print(f"Month Income       : {money(month_income_base)}")
    print(f"Month Expense      : {money(month_expense_base)}")
    print(f"Month Balance      : {money(month_balance_base)}")
    print(f"Top Expense        : {top_category}")
    print(f"Top Category Amt   : {money(top_category_amount_base)}")
    print("------------------------------------------")
    print(f"Monthly Budget     : {money(monthly_budget_base)}")
    print(f"Budget Remaining   : {money(budget_remaining_base)}")
    print(f"Budget Used        : {budget_used:.1f}%")

    if monthly_budget_base > 0:
        if month_expense_base > monthly_budget_base:
            print("Budget Status      : OVER BUDGET")
        elif budget_used >= 80:
            print("Budget Status      : WARNING - 80% USED")
        else:
            print("Budget Status      : OK")
    else:
        print("Budget Status      : Not Set")

    print("------------------------------------------")
    print(f"Outstanding Lent   : {money(total_lent)}")
    print(f"Outstanding Borrow : {money(total_borrowed)}")
    print("------------------------------------------")
    print("[1] Change Dashboard Currency")
    print("[2] Back to Main Menu")
    print("==========================================")


def show_dashboard():
    # Always open in the base currency, as requested.
    # The currency option changes display only; stored/base calculations stay unchanged.
    display_currency = get_base_currency()

    while True:
        _render_dashboard(display_currency)
        choice = input("Choose option [1/2]: ").strip()

        if choice == "1":
            new_currency = choose_currency("Choose dashboard display currency")
            if new_currency != get_base_currency():
                ensure_currency_rate(new_currency)
            display_currency = new_currency
        elif choice == "2" or choice == "":
            return
        else:
            print("Invalid option. Please choose 1 or 2.")

def financial_analysis():

    print(
        "\n=========================================="
    )

    print(
        "          FINANCIAL ANALYSIS"
    )

    print(
        "=========================================="
    )

    if not transactions:

        print(
            "No transaction data available."
        )

        return

    total_income = sum(
        get_amount(t)
        for t in transactions
        if t.get("type") == "Income"
    )

    total_expense = sum(
        get_amount(t)
        for t in transactions
        if t.get("type") == "Expense"
    )

    balance = (
        total_income
        - total_expense
    )

    total_transactions = len(
        transactions
    )

    expense_transactions = [
        t
        for t in transactions
        if t.get("type") == "Expense"
    ]

    income_transactions = [
        t
        for t in transactions
        if t.get("type") == "Income"
    ]

    if total_income > 0:

        savings_rate = (
            balance
            / total_income
            * 100
        )

        expense_ratio = (
            total_expense
            / total_income
            * 100
        )

    else:

        savings_rate = 0

        expense_ratio = 0

    if expense_transactions:

        highest_transaction = max(
            expense_transactions,
            key=get_amount
        )

        highest_amount = get_amount(
            highest_transaction
        )

    else:

        highest_transaction = None

        highest_amount = 0

    category_totals = {}

    for t in expense_transactions:

        category = t.get(
            "category",
            "Uncategorized"
        )

        category_totals[category] = (
            category_totals.get(
                category,
                0
            )
            + get_amount(t)
        )

    if category_totals:

        top_category = max(
            category_totals,
            key=category_totals.get
        )

        top_category_amount = (
            category_totals[
                top_category
            ]
        )

    else:

        top_category = "None"

        top_category_amount = 0

    if expense_transactions:

        average_expense = (
            total_expense
            / len(
                expense_transactions
            )
        )

    else:

        average_expense = 0

    if income_transactions:

        average_income = (
            total_income
            / len(
                income_transactions
            )
        )

    else:

        average_income = 0

    monthly_data = {}

    for t in transactions:

        date_text = str(
            t.get("date", "")
        )

        if len(date_text) >= 10:

            month = date_text[3:10]

        else:

            continue

        monthly_data.setdefault(
            month,
            {
                "income": 0,
                "expense": 0
            }
        )

        amount = get_amount(t)

        if t.get("type") == "Income":

            monthly_data[month][
                "income"
            ] += amount

        elif t.get("type") == "Expense":

            monthly_data[month][
                "expense"
            ] += amount

    print(
        "\n========== OVERALL ANALYSIS =========="
    )

    print(
        f"Total Income           : "
        f"RM {total_income:.2f}"
    )

    print(
        f"Total Expense          : "
        f"RM {total_expense:.2f}"
    )

    print(
        f"Net Balance            : "
        f"RM {balance:.2f}"
    )

    print(
        f"Total Transactions     : "
        f"{total_transactions}"
    )

    print(
        f"Savings Rate           : "
        f"{savings_rate:.1f}%"
    )

    print(
        f"Expense / Income Ratio : "
        f"{expense_ratio:.1f}%"
    )

    print(
        f"Average Income         : "
        f"RM {average_income:.2f}"
    )

    print(
        f"Average Expense        : "
        f"RM {average_expense:.2f}"
    )

    print(
        "\n========== TOP SPENDING =========="
    )

    print(
        f"Top Category           : "
        f"{top_category}"
    )

    print(
        f"Top Category Amount    : "
        f"RM {top_category_amount:.2f}"
    )

    if highest_transaction:

        print(
            f"Highest Expense        : "
            f"RM {highest_amount:.2f}"
        )

        print(
            f"Highest Expense ID     : "
            f"{highest_transaction.get('id', '')}"
        )

        print(
            f"Highest Expense Date   : "
            f"{highest_transaction.get('date', '')}"
        )

        print(
            f"Highest Expense Desc.  : "
            f"{highest_transaction.get('description', '')}"
        )

    else:

        print(
            "Highest Expense        : None"
        )

    print(
        "\n========== CATEGORY ANALYSIS =========="
    )

    if category_totals:

        sorted_categories = sorted(
            category_totals.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, amount in (
            sorted_categories
        ):

            if total_expense > 0:

                percentage = (
                    amount
                    / total_expense
                    * 100
                )

            else:

                percentage = 0

            print(
                f"{category:<20} "
                f"RM {amount:>10.2f} "
                f"({percentage:.1f}%)"
            )

    else:

        print(
            "No expense category data."
        )

    print(
        "\n========== MONTHLY ANALYSIS =========="
    )

    if monthly_data:

        sorted_months = sorted(
            monthly_data.items()
        )

        for month, data in (
            sorted_months
        ):

            month_balance = (
                data["income"]
                - data["expense"]
            )

            print(
                f"{month} | "
                f"Income: "
                f"RM {data['income']:.2f} | "
                f"Expense: "
                f"RM {data['expense']:.2f} | "
                f"Balance: "
                f"RM {month_balance:.2f}"
            )

    else:

        print(
            "No monthly data."
        )

    total_lent = sum(
        float(
            loan.get(
                "remaining",
                0
            )
        )
        for loan in loans
        if loan.get("type") == "Lending"
    )

    total_borrowed = sum(
        float(
            loan.get(
                "remaining",
                0
            )
        )
        for loan in loans
        if loan.get("type") == "Borrowing"
    )

    print(
        "\n========== LOAN ANALYSIS =========="
    )

    print(
        f"Outstanding Lending : "
        f"RM {total_lent:.2f}"
    )

    print(
        f"Outstanding Borrowing: "
        f"RM {total_borrowed:.2f}"
    )

    print(
        f"Net Loan Position    : "
        f"RM {total_lent - total_borrowed:.2f}"
    )

    print(
        "\n========== FINANCIAL STATUS =========="
    )

    if balance > 0:

        print(
            "Status: POSITIVE - "
            "Income is higher than expenses."
        )

    elif balance < 0:

        print(
            "Status: NEGATIVE - "
            "Expenses are higher than income."
        )

    else:

        print(
            "Status: BREAK-EVEN"
        )

    if savings_rate >= 20:

        print(
            "Savings Health: GOOD"
        )

    elif savings_rate >= 10:

        print(
            "Savings Health: MODERATE"
        )

    elif savings_rate > 0:

        print(
            "Savings Health: LOW"
        )

    else:

        print(
            "Savings Health: "
            "NO POSITIVE SAVINGS"
        )

    print(
        "\n=========================================="
    )

    print(
        "1. Export Financial Analysis to PDF"
    )

    print("2. Back")

    choice = input(
        "Choose option: "
    ).strip()

    if choice == "1":

        export_financial_analysis_pdf(
            total_income,
            total_expense,
            balance,
            total_transactions,
            savings_rate,
            expense_ratio,
            average_income,
            average_expense,
            top_category,
            top_category_amount,
            highest_transaction,
            category_totals,
            monthly_data,
            total_lent,
            total_borrowed
        )

def export_financial_analysis_pdf(
    total_income,
    total_expense,
    balance,
    total_transactions,
    savings_rate,
    expense_ratio,
    average_income,
    average_expense,
    top_category,
    top_category_amount,
    highest_transaction,
    category_totals,
    monthly_data,
    total_lent,
    total_borrowed
):

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
            "ReportLab is not installed."
        )

        print(
            "Use: pip install reportlab"
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

    filepath = os.path.join(
        PDF_FOLDER,
        f"MoneyTracker_Analysis_{timestamp}.pdf"
    )

    try:

        document = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
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
            Paragraph(
                "Financial Analysis Report",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        summary_data = [

            [
                "Financial Metric",
                "Value"
            ],

            [
                "Total Income",
                f"RM {total_income:.2f}"
            ],

            [
                "Total Expense",
                f"RM {total_expense:.2f}"
            ],

            [
                "Net Balance",
                f"RM {balance:.2f}"
            ],

            [
                "Transactions",
                str(total_transactions)
            ],

            [
                "Savings Rate",
                f"{savings_rate:.1f}%"
            ],

            [
                "Expense / Income",
                f"{expense_ratio:.1f}%"
            ],

            [
                "Average Income",
                f"RM {average_income:.2f}"
            ],

            [
                "Average Expense",
                f"RM {average_expense:.2f}"
            ],

            [
                "Top Category",
                top_category
            ],

            [
                "Top Category Amount",
                f"RM {top_category_amount:.2f}"
            ],

            [
                "Outstanding Lending",
                f"RM {total_lent:.2f}"
            ],

            [
                "Outstanding Borrowing",
                f"RM {total_borrowed:.2f}"
            ]
        ]

        table = Table(
            summary_data,
            colWidths=[
                250,
                220
            ]
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
                        9
                    )
                ]
            )
        )

        elements.append(
            table
        )

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                "Category Analysis",
                styles["Heading3"]
            )
        )

        category_table = [
            [
                "Category",
                "Amount",
                "Percentage"
            ]
        ]

        for category, amount in sorted(
            category_totals.items(),
            key=lambda x: x[1],
            reverse=True
        ):

            if total_expense > 0:

                percentage = (
                    amount
                    / total_expense
                    * 100
                )

            else:

                percentage = 0

            category_table.append(
                [
                    category,
                    f"RM {amount:.2f}",
                    f"{percentage:.1f}%"
                ]
            )

        if len(
            category_table
        ) > 1:

            table2 = Table(
                category_table,
                repeatRows=1
            )

            table2.setStyle(
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
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            8
                        )
                    ]
                )
            )

            elements.append(
                table2
            )

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                "Monthly Analysis",
                styles["Heading3"]
            )
        )

        monthly_table = [
            [
                "Month",
                "Income",
                "Expense",
                "Balance"
            ]
        ]

        for month, data in sorted(
            monthly_data.items()
        ):

            month_balance = (
                data["income"]
                - data["expense"]
            )

            monthly_table.append(
                [
                    month,
                    f"RM {data['income']:.2f}",
                    f"RM {data['expense']:.2f}",
                    f"RM {month_balance:.2f}"
                ]
            )

        if len(
            monthly_table
        ) > 1:

            table3 = Table(
                monthly_table,
                repeatRows=1
            )

            table3.setStyle(
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
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            8
                        )
                    ]
                )
            )

            elements.append(
                table3
            )

        if highest_transaction:

            elements.append(
                Spacer(1, 15)
            )

            elements.append(
                Paragraph(
                    "Highest Expense Transaction",
                    styles["Heading3"]
                )
            )

            elements.append(
                Paragraph(
                    f"ID: "
                    f"{highest_transaction.get('id', '')}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"Date: "
                    f"{highest_transaction.get('date', '')}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"Category: "
                    f"{highest_transaction.get('category', '')}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"Amount: "
                    f"RM "
                    f"{get_amount(highest_transaction):.2f}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"Description: "
                    f"{highest_transaction.get('description', '')}",
                    styles["Normal"]
                )
            )

        elements.append(
            Spacer(1, 15)
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
            "\nFinancial Analysis PDF "
            "exported successfully!"
        )

        print(
            f"File: {filepath}"
        )

    except Exception as error:

        print(
            "\nFinancial Analysis PDF "
            "export failed."
        )

        print(
            f"Error: {error}"
        )
