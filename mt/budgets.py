# ==========================================================
# MONEY TRACKER - BUDGETS MODULE
# ==========================================================
from common import *

def save_budgets():

    save_json(
        BUDGET_FILE,
        budgets
    )

def save_category_budgets():

    save_json(
        CATEGORY_BUDGET_FILE,
        category_budgets
    )

def set_monthly_budget():

    current_month = datetime.now().strftime(
        "%m-%Y"
    )

    print(
        "\n========== SET MONTHLY BUDGET =========="
    )

    print(
        f"Current Month: {current_month}"
    )

    try:

        amount = float(
            input(
                "Enter monthly budget: RM "
            ).strip()
        )

        if amount < 0:

            print(
                "Budget cannot be negative."
            )

            return

        budgets[current_month] = amount

        save_budgets()

        print(
            f"Budget saved successfully: "
            f"RM {amount:.2f}"
        )

    except ValueError:

        print(
            "Invalid budget amount."
        )

def show_budget():

    current_month = datetime.now().strftime(
        "%m-%Y"
    )

    budget = float(
        budgets.get(
            current_month,
            0
        )
    )

    expense = sum(
        get_amount(t)
        for t in transactions
        if (
            t.get("type") == "Expense"
            and str(
                t.get("date", "")
            ).endswith(current_month)
        )
    )

    remaining = (
        budget - expense
    )

    if budget > 0:

        percentage = (
            expense
            / budget
            * 100
        )

    else:

        percentage = 0

    print(
        "\n========== BUDGET STATUS =========="
    )

    print(
        f"Month          : {current_month}"
    )

    print(
        f"Monthly Budget : RM {budget:.2f}"
    )

    print(
        f"Expense        : RM {expense:.2f}"
    )

    print(
        f"Remaining      : RM {remaining:.2f}"
    )

    print(
        f"Budget Used    : {percentage:.1f}%"
    )

    if budget == 0:

        print(
            "Budget Status  : Not Set"
        )

    elif expense > budget:

        print(
            f"WARNING: OVER BUDGET by "
            f"RM {expense - budget:.2f}"
        )

    elif percentage >= 80:

        print(
            "WARNING: 80% OF BUDGET USED"
        )

    else:

        print(
            "Budget Status  : OK"
        )

def set_category_budget():

    current_month = datetime.now().strftime(
        "%m-%Y"
    )

    print(
        "\n======= SET CATEGORY BUDGET ======="
    )

    print(
        f"Month: {current_month}"
    )

    for number, category in enumerate(
        EXPENSE_CATEGORIES,
        1
    ):

        print(
            f"{number}. {category}"
        )

    try:

        number = int(
            input(
                "Choose category: "
            ).strip()
        )

        if not (
            1
            <= number
            <= len(EXPENSE_CATEGORIES)
        ):

            print(
                "Invalid category."
            )

            return

        category = EXPENSE_CATEGORIES[
            number - 1
        ]

        amount = float(
            input(
                f"Enter budget for "
                f"{category}: RM "
            ).strip()
        )

        if amount < 0:

            print(
                "Budget cannot be negative."
            )

            return

        category_budgets.setdefault(
            current_month,
            {}
        )[category] = amount

        save_category_budgets()

        print(
            f"{category} budget saved: "
            f"RM {amount:.2f}"
        )

    except ValueError:

        print(
            "Invalid input."
        )

def show_category_budgets():

    current_month = datetime.now().strftime(
        "%m-%Y"
    )

    print(
        "\n======= CATEGORY BUDGET STATUS ======="
    )

    print(
        f"Month: {current_month}"
    )

    budgets_for_month = (
        category_budgets.get(
            current_month,
            {}
        )
    )

    if not budgets_for_month:

        print(
            "No category budgets set."
        )

        return

    for category, budget_value in (
        budgets_for_month.items()
    ):

        budget = float(
            budget_value
        )

        spent = 0

        for t in transactions:

            if (
                t.get("type") == "Expense"
                and str(
                    t.get("date", "")
                ).endswith(
                    current_month
                )
                and str(
                    t.get("category", "")
                ).lower()
                == category.lower()
            ):

                spent += get_amount(t)

        remaining = (
            budget - spent
        )

        if budget > 0:

            used = (
                spent
                / budget
                * 100
            )

        else:

            used = 0

        print(
            "\n----------------------------------------"
        )

        print(
            f"Category     : {category}"
        )

        print(
            f"Budget       : RM {budget:.2f}"
        )

        print(
            f"Spent        : RM {spent:.2f}"
        )

        print(
            f"Remaining    : RM {remaining:.2f}"
        )

        print(
            f"Used         : {used:.1f}%"
        )

        if budget == 0:

            print(
                "Status       : Budget is zero"
            )

        elif spent > budget:

            print(
                "Status       : OVER BUDGET"
            )

        elif used >= 80:

            print(
                "Status       : "
                "WARNING - 80% USED"
            )

        else:

            print(
                "Status       : OK"
            )
