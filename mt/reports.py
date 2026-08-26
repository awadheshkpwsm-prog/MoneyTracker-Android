# ==========================================================
# MONEY TRACKER - REPORTS MODULE
# ==========================================================
from common import *

def monthly_report():

    month = input(
        "Enter month and year (MM-YYYY): "
    ).strip()

    income = 0

    expense = 0

    count = 0

    results = []

    for t in transactions:

        if str(
            t.get("date", "")
        ).endswith(month):

            amount = get_amount(t)

            count += 1

            results.append(t)

            if t.get("type") == "Income":

                income += amount

            elif t.get("type") == "Expense":

                expense += amount

    print(
        "\n========== MONTHLY REPORT =========="
    )

    print(
        f"Month        : {month}"
    )

    print(
        f"Total Income : RM {income:.2f}"
    )

    print(
        f"Total Expense: RM {expense:.2f}"
    )

    print(
        f"Balance      : RM "
        f"{income - expense:.2f}"
    )

    print(
        f"Transactions : {count}"
    )

    if results:

        print(
            "\n1. Export Monthly Report to PDF"
        )

        print("2. Back")

        choice = input(
            "Choose option: "
        ).strip()

        if choice == "1":

            export_transactions_to_pdf(
                results,
                f"Monthly Report - {month}"
            )

    else:

        print(
            "\nNo transactions found "
            "for this month."
        )

def category_expense_report():

    categories = {}

    results = []

    for t in transactions:

        if t.get("type") == "Expense":

            category = t.get(
                "category",
                "Uncategorized"
            )

            amount = get_amount(t)

            categories[category] = (
                categories.get(
                    category,
                    0
                )
                + amount
            )

            results.append(t)

    print(
        "\n===== CATEGORY EXPENSE REPORT ====="
    )

    if not categories:

        print(
            "No expense transactions found."
        )

        return

    total = 0

    for category, amount in categories.items():

        print(
            f"{category:<20} "
            f"RM {amount:.2f}"
        )

        total += amount

    print(
        "-----------------------------------"
    )

    print(
        f"TOTAL EXPENSE: RM {total:.2f}"
    )

    print(
        "\n1. Export Category Report to PDF"
    )

    print("2. Back")

    choice = input(
        "Choose option: "
    ).strip()

    if choice == "1":

        export_transactions_to_pdf(
            results,
            "Category Expense Report"
        )

def income_expense_summary():

    income = sum(
        get_amount(t)
        for t in transactions
        if t.get("type") == "Income"
    )

    expense = sum(
        get_amount(t)
        for t in transactions
        if t.get("type") == "Expense"
    )

    balance = (
        income - expense
    )

    print(
        "\n===== INCOME / EXPENSE SUMMARY ====="
    )

    print(
        f"Total Income  : RM {income:.2f}"
    )

    print(
        f"Total Expense : RM {expense:.2f}"
    )

    print(
        f"Balance       : RM {balance:.2f}"
    )

    print(
        "\n1. Export Summary to PDF"
    )

    print("2. Back")

    choice = input(
        "Choose option: "
    ).strip()

    if choice == "1":

        export_transactions_to_pdf(
            transactions,
            "Income Expense Summary"
        )

def export_combined_report_pdf():

    if (
        not transactions
        and not loans
    ):

        print(
            "No data available "
            "for combined report."
        )

        return

    try:

        from reportlab.lib.pagesizes import A4

        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            PageBreak
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
        f"MoneyTracker_Combined_{timestamp}.pdf"
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

        total_lending = sum(
            float(
                l.get(
                    "remaining",
                    0
                )
            )
            for l in loans
            if l.get("type") == "Lending"
        )

        total_borrowing = sum(
            float(
                l.get(
                    "remaining",
                    0
                )
            )
            for l in loans
            if l.get("type") == "Borrowing"
        )

        elements.append(
            Paragraph(
                "MONEY TRACKER",
                styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                "COMBINED FINANCIAL REPORT",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        summary = [

            [
                "Summary",
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
                "Balance",
                f"RM {balance:.2f}"
            ],

            [
                "Transactions",
                str(len(transactions))
            ],

            [
                "Outstanding Lending",
                f"RM {total_lending:.2f}"
            ],

            [
                "Outstanding Borrowing",
                f"RM {total_borrowing:.2f}"
            ]
        ]

        summary_table = Table(
            summary
        )

        summary_table.setStyle(
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
            summary_table
        )

        elements.append(
            Spacer(1, 20)
        )

        elements.append(
            Paragraph(
                "Transactions",
                styles["Heading3"]
            )
        )

        transaction_table = [

            [
                "ID",
                "Date",
                "Type",
                "Category",
                "Amount"
            ]
        ]

        for t in transactions:

            transaction_table.append(
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

                    f"RM "
                    f"{get_amount(t):.2f}"
                ]
            )

        table = Table(
            transaction_table,
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
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7
                    )
                ]
            )
        )

        elements.append(
            table
        )

        elements.append(
            PageBreak()
        )

        elements.append(
            Paragraph(
                "Lending / Borrowing",
                styles["Heading3"]
            )
        )

        loan_table = [

            [
                "Name",
                "Type",
                "Original",
                "Remaining",
                "Status"
            ]
        ]

        for loan in loans:

            original = float(
                loan.get(
                    "amount",
                    0
                )
            )

            remaining = float(
                loan.get(
                    "remaining",
                    original
                )
            )

            status = (
                "PAID"
                if remaining <= 0
                else "OPEN"
            )

            loan_table.append(
                [
                    str(
                        loan.get(
                            "name",
                            ""
                        )
                    ),

                    str(
                        loan.get(
                            "type",
                            ""
                        )
                    ),

                    f"RM {original:.2f}",

                    f"RM {remaining:.2f}",

                    status
                ]
            )

        if len(
            loan_table
        ) > 1:

            loan_pdf_table = Table(
                loan_table,
                repeatRows=1
            )

            loan_pdf_table.setStyle(
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
                loan_pdf_table
            )

        elements.append(
            Spacer(1, 20)
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
            "\nCombined Financial Report "
            "exported successfully!"
        )

        print(
            f"File: {filepath}"
        )

    except Exception as error:

        print(
            "\nCombined report export failed."
        )

        print(
            f"Error: {error}"
        )
