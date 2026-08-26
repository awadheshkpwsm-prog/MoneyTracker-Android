# ==========================================================
# MONEY TRACKER - MENUS
# ==========================================================
from common import *
from transactions import *
from budgets import *
from loans import *
from reports import *
from analytics import *
from currency import *
from accounts import *

def show_reports():

    while True:

        print(
            "\n========== REPORTS =========="
        )

        print(
            "1. Monthly Report"
        )

        print(
            "2. Category Expense Report"
        )

        print(
            "3. Income / Expense Summary"
        )

        print(
            "4. Lending / Borrowing Report"
        )

        print(
            "5. Financial Analysis"
        )

        print(
            "6. Export All Transactions PDF"
        )

        print(
            "7. Combined Financial Report PDF"
        )

        print(
            "8. Back to Main Menu"
        )

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            monthly_report()

        elif choice == "2":

            category_expense_report()

        elif choice == "3":

            income_expense_summary()

        elif choice == "4":

            show_loan_report()

        elif choice == "5":

            financial_analysis()

        elif choice == "6":

            export_all_transactions_pdf()

        elif choice == "7":

            export_combined_report_pdf()

        elif choice == "8":

            return

        else:

            print(
                "Invalid option. "
                "Please choose 1-8."
            )

def loan_menu():

    while True:

        print(
            "\n========== LENDING / BORROWING =========="
        )

        print(
            "1. Add Lending / Borrowing"
        )

        print(
            "2. View All"
        )

        print(
            "3. Record Repayment"
        )

        print(
            "4. Edit Loan"
        )

        print(
            "5. Delete Loan"
        )

        print(
            "6. Loan Report"
        )

        print(
            "7. Back to Main Menu"
        )

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            add_loan()

        elif choice == "2":

            show_loans()

        elif choice == "3":

            record_repayment()

        elif choice == "4":

            edit_loan()

        elif choice == "5":

            delete_loan()

        elif choice == "6":

            show_loan_report()

        elif choice == "7":

            return

        else:

            print(
                "Invalid option. "
                "Please choose 1-7."
            )

def transaction_management_menu():

    while True:

        print(
            "\n=========================================="
        )

        print(
            "        TRANSACTION MANAGEMENT"
        )

        print(
            "=========================================="
        )

        print(
            "1. Show All Transactions"
        )

        print(
            "2. Search Transactions"
        )

        print(
            "3. Edit Transaction"
        )

        print(
            "4. Delete Transaction"
        )

        print(
            "5. Advanced Transaction Filter"
        )

        print(
            "6. Sort Transactions"
        )

        print(
            "7. Quick Date Filter"
        )

        print(
            "8. Combined Search + Filter"
        )

        print(
            "9. Export All Transactions PDF"
        )

        print(
            "10. Back to Main Menu"
        )

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            show_transactions()

        elif choice == "2":

            search_transactions()

        elif choice == "3":

            edit_transaction()

        elif choice == "4":

            delete_transaction()

        elif choice == "5":

            advanced_transaction_filter()

        elif choice == "6":

            sort_transactions()

        elif choice == "7":

            quick_date_filter()

        elif choice == "8":

            combined_transaction_filter()

        elif choice == "9":

            export_all_transactions_pdf()

        elif choice == "10":

            return

        else:

            print(
                "Invalid option. "
                "Please choose 1-10."
            )

def main_menu():

    while True:

        print(
            "\n=========================================="
        )

        print(
            "          MONEY TRACKER"
        )

        print(
            "=========================================="
        )

        print(
            "1. Dashboard"
        )

        print(
            "2. Add Transaction"
        )

        print(
            "3. Transaction Management"
        )

        print(
            "4. Reports"
        )

        print(
            "5. Set Monthly Budget"
        )

        print(
            "6. Show Budget"
        )

        print(
            "7. Set Category Budget"
        )

        print(
            "8. Show Category Budgets"
        )

        print(
            "9. Lending / Borrowing"
        )

        print(
            "10. Advanced Transaction Filter"
        )

        print(
            "11. Export All Transactions PDF"
        )

        print(
            "12. Combined Financial Report PDF"
        )

        print(
            "13. Financial Analysis"
        )

        print(
            "14. Sort Transactions"
        )

        print(
            "15. Quick Date Filter"
        )

        print(
            "16. Combined Search + Filter"
        )

        print(
            "17. Multi-Currency"
        )

        print(
            "18. Accounts / Wallets"
        )

        print(
            "19. Exit"
        )

        print(
            "=========================================="
        )

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            show_dashboard()

        elif choice == "2":

            add_transaction()

        elif choice == "3":

            transaction_management_menu()

        elif choice == "4":

            show_reports()

        elif choice == "5":

            set_monthly_budget()

        elif choice == "6":

            show_budget()

        elif choice == "7":

            set_category_budget()

        elif choice == "8":

            show_category_budgets()

        elif choice == "9":

            loan_menu()

        elif choice == "10":

            advanced_transaction_filter()

        elif choice == "11":

            export_all_transactions_pdf()

        elif choice == "12":

            export_combined_report_pdf()

        elif choice == "13":

            financial_analysis()

        elif choice == "14":

            sort_transactions()

        elif choice == "15":

            quick_date_filter()

        elif choice == "16":

            combined_transaction_filter()

        elif choice == "17":

            currency_menu()

        elif choice == "18":

            account_menu()

        elif choice == "19":

            print(
                "Thank you for using "
                "Money Tracker!"
            )

            break

        else:

            print(
                "Invalid option. "
                "Please choose 1-19."
            )
