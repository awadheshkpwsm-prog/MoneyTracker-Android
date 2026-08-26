# ==========================================================
# MONEY TRACKER - LOANS MODULE
# ==========================================================
from common import *

def save_loans():

    save_json(
        LOAN_FILE,
        loans
    )

def add_loan():

    print(
        "\n========== ADD LENDING / BORROWING =========="
    )

    print(
        "1. Lending - Money you gave to someone"
    )

    print(
        "2. Borrowing - Money you received from someone"
    )

    choice = input(
        "Choose type: "
    ).strip()

    if choice == "1":

        loan_type = "Lending"

    elif choice == "2":

        loan_type = "Borrowing"

    else:

        print(
            "Invalid choice."
        )

        return

    name = input(
        "Enter person/name: "
    ).strip()

    if not name:

        print(
            "Name cannot be empty."
        )

        return

    try:

        amount = float(
            input(
                "Enter amount: RM "
            ).strip()
        )

        if amount <= 0:

            print(
                "Amount must be greater "
                "than zero."
            )

            return

    except ValueError:

        print(
            "Invalid amount."
        )

        return

    description = input(
        "Description (optional): "
    ).strip()

    date = datetime.now().strftime(
        "%d-%m-%Y"
    )

    loans.append(
        {
            "name": name,
            "type": loan_type,
            "amount": amount,
            "remaining": amount,
            "date": date,
            "description": description,
            "repayments": []
        }
    )

    save_loans()

    print(
        f"{loan_type} saved successfully!"
    )

def show_loans():

    print(
        "\n========== LENDING / BORROWING =========="
    )

    if not loans:

        print(
            "No lending or borrowing records."
        )

        return

    for number, loan in enumerate(
        loans,
        1
    ):

        amount = float(
            loan.get(
                "amount",
                0
            )
        )

        remaining = float(
            loan.get(
                "remaining",
                amount
            )
        )

        paid = (
            amount
            - remaining
        )

        if remaining <= 0:

            status = "PAID"

        else:

            status = "OPEN"

        print(
            "\n------------------------------------------"
        )

        print(
            f"{number}. Name        : "
            f"{loan.get('name', 'Unknown')}"
        )

        print(
            f"Type            : "
            f"{loan.get('type', 'Unknown')}"
        )

        print(
            f"Original Amount : "
            f"RM {amount:.2f}"
        )

        print(
            f"Paid            : "
            f"RM {paid:.2f}"
        )

        print(
            f"Remaining       : "
            f"RM {remaining:.2f}"
        )

        print(
            f"Date            : "
            f"{loan.get('date', '')}"
        )

        print(
            f"Description     : "
            f"{loan.get('description', '')}"
        )

        print(
            f"Status          : {status}"
        )

def record_repayment():

    show_loans()

    if not loans:

        return

    try:

        number = int(
            input(
                "\nEnter loan number "
                "for repayment: "
            ).strip()
        )

        if not (
            1
            <= number
            <= len(loans)
        ):

            print(
                "Invalid loan number."
            )

            return

        loan = loans[number - 1]

        remaining = float(
            loan.get(
                "remaining",
                loan.get(
                    "amount",
                    0
                )
            )
        )

        if remaining <= 0:

            print(
                "This loan is already "
                "fully paid."
            )

            return

        print(
            f"Remaining amount: "
            f"RM {remaining:.2f}"
        )

        payment = float(
            input(
                "Enter repayment amount: RM "
            ).strip()
        )

        if payment <= 0:

            print(
                "Repayment must be "
                "greater than zero."
            )

            return

        if payment > remaining:

            print(
                f"Repayment cannot exceed "
                f"remaining amount "
                f"RM {remaining:.2f}."
            )

            return

        loan["remaining"] = round(
            remaining - payment,
            2
        )

        loan.setdefault(
            "repayments",
            []
        )

        loan["repayments"].append(
            {
                "date": datetime.now().strftime(
                    "%d-%m-%Y"
                ),
                "amount": payment
            }
        )

        save_loans()

        if loan["remaining"] == 0:

            print(
                "Repayment saved. "
                "Loan is now FULLY PAID!"
            )

        else:

            print(
                f"Repayment saved. "
                f"Remaining: RM "
                f"{loan['remaining']:.2f}"
            )

    except ValueError:

        print(
            "Invalid input."
        )

def edit_loan():

    show_loans()

    if not loans:

        return

    try:

        number = int(
            input(
                "\nEnter loan number to edit: "
            ).strip()
        )

        if not (
            1
            <= number
            <= len(loans)
        ):

            print(
                "Invalid loan number."
            )

            return

        loan = loans[number - 1]

        print(
            "\nPress Enter to keep "
            "the old value."
        )

        name = input(
            f"Name "
            f"[{loan.get('name', '')}]: "
        ).strip()

        description = input(
            f"Description "
            f"[{loan.get('description', '')}]: "
        ).strip()

        if name:

            loan["name"] = name

        if description:

            loan["description"] = (
                description
            )

        save_loans()

        print(
            "Loan updated successfully!"
        )

    except ValueError:

        print(
            "Please enter a valid number."
        )

def delete_loan():

    show_loans()

    if not loans:

        return

    try:

        number = int(
            input(
                "\nEnter loan number "
                "to delete: "
            ).strip()
        )

        if not (
            1
            <= number
            <= len(loans)
        ):

            print(
                "Invalid loan number."
            )

            return

        confirm = input(
            "Type YES to permanently delete: "
        ).strip()

        if confirm.upper() == "YES":

            deleted = loans.pop(
                number - 1
            )

            save_loans()

            print(
                f"Deleted loan for "
                f"{deleted.get('name', 'Unknown')}."
            )

        else:

            print(
                "Delete cancelled."
            )

    except ValueError:

        print(
            "Please enter a valid number."
        )

def show_loan_report():

    total_lending = 0

    total_borrowing = 0

    paid_lending = 0

    paid_borrowing = 0

    open_lending = 0

    open_borrowing = 0

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

        paid = (
            original
            - remaining
        )

        if loan.get("type") == "Lending":

            total_lending += original

            paid_lending += paid

            open_lending += remaining

        elif loan.get("type") == "Borrowing":

            total_borrowing += original

            paid_borrowing += paid

            open_borrowing += remaining

    print(
        "\n========== LENDING / BORROWING REPORT =========="
    )

    print(
        f"Total Lent          : "
        f"RM {total_lending:.2f}"
    )

    print(
        f"Recovered           : "
        f"RM {paid_lending:.2f}"
    )

    print(
        f"Outstanding Lending : "
        f"RM {open_lending:.2f}"
    )

    print(
        "-----------------------------------------------"
    )

    print(
        f"Total Borrowed      : "
        f"RM {total_borrowing:.2f}"
    )

    print(
        f"Repaid              : "
        f"RM {paid_borrowing:.2f}"
    )

    print(
        f"Outstanding Borrow  : "
        f"RM {open_borrowing:.2f}"
    )

    print(
        "-----------------------------------------------"
    )

    print(
        f"Net Outstanding     : "
        f"RM {open_lending - open_borrowing:.2f}"
    )

    print(
        f"Total Loan Records  : "
        f"{len(loans)}"
    )

    print(
        "\n1. Export Loan Report to PDF"
    )

    print("2. Back")

    choice = input(
        "Choose option: "
    ).strip()

    if choice == "1":

        export_loan_report_pdf()

def export_loan_report_pdf():

    if not loans:

        print(
            "No loan data available."
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
        f"MoneyTracker_Loan_{timestamp}.pdf"
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
                "Lending / Borrowing Report",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        table_data = [
            [
                "Name",
                "Type",
                "Original",
                "Paid",
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

            paid = (
                original
                - remaining
            )

            status = (
                "PAID"
                if remaining <= 0
                else "OPEN"
            )

            table_data.append(
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

                    f"RM {paid:.2f}",

                    f"RM {remaining:.2f}",

                    status
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
                        8
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
            "\nLoan PDF exported successfully!"
        )

        print(
            f"File: {filepath}"
        )

    except Exception as error:

        print(
            "\nLoan PDF export failed."
        )

        print(
            f"Error: {error}"
        )
