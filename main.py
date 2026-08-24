"""Money Tracker Android UI.
The original modular mt/ backend is preserved and reused.
"""
import os
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


class MoneyTrackerApp(App):
    title = "Money Tracker"

    def build(self):
        os.environ["MONEY_TRACKER_DATA_DIR"] = self.user_data_dir
        # Import after setting the writable Android data directory.
        import mt.common as common
        import mt.accounts as accounts_mod
        import mt.currency as currency_mod
        self.common = common
        self.accounts = accounts_mod
        self.currency = currency_mod
        self.accounts.ensure_accounts()

        sm = ScreenManager()
        sm.add_widget(DashboardScreen(name="dashboard", app=self))
        sm.add_widget(TransactionsScreen(name="transactions", app=self))
        sm.add_widget(AddTransactionScreen(name="add", app=self))
        sm.add_widget(AccountsScreen(name="accounts", app=self))
        sm.add_widget(CurrencyScreen(name="currency", app=self))
        self.sm = sm
        return sm

    def refresh(self):
        for screen in self.sm.screens:
            if hasattr(screen, "refresh"):
                screen.refresh()

    def toast(self, text):
        Popup(title="Money Tracker", content=Label(text=text), size_hint=(.88, .3)).open()


class BaseScreen(Screen):
    def __init__(self, app, **kwargs):
        self.app = app
        super().__init__(**kwargs)

    def root(self, title):
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        box.add_widget(Label(text=title, font_size=dp(24), size_hint_y=None, height=dp(48)))
        return box

    def nav(self, box):
        row = GridLayout(cols=3, size_hint_y=None, height=dp(48), spacing=dp(5))
        for text, target in [("Dashboard", "dashboard"), ("Transactions", "transactions"), ("Accounts", "accounts")]:
            b = Button(text=text)
            b.bind(on_release=lambda _, t=target: setattr(self.manager, "current", t))
            row.add_widget(b)
        box.add_widget(row)


class DashboardScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.body = None
        self.display_currency = None

    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        base = self.app.common.get_base_currency()
        self.display_currency = self.display_currency or base
        transactions = self.app.common.transactions
        income = sum(self.app.common.get_base_amount(t) for t in transactions if t.get("type") == "Income")
        expense = sum(self.app.common.get_base_amount(t) for t in transactions if t.get("type") == "Expense")
        balance = income - expense
        month = datetime.now().strftime("%m-%Y")
        mi = sum(self.app.common.get_base_amount(t) for t in transactions if t.get("type") == "Income" and str(t.get("date", "")).endswith(month))
        me = sum(self.app.common.get_base_amount(t) for t in transactions if t.get("type") == "Expense" and str(t.get("date", "")).endswith(month))
        display = self.display_currency
        def money(v):
            try:
                v = self.app.currency.convert_from_base(v, display) if display != base else v
            except Exception:
                pass
            return f"{v:.2f} {display}"
        root = self.root("Money Tracker")
        root.add_widget(Label(text=f"Display: {display}   |   Base: {base}", size_hint_y=None, height=dp(32)))
        grid = GridLayout(cols=2, size_hint_y=None, height=dp(190), spacing=dp(6))
        for k, v in [("Total Income", money(income)), ("Total Expense", money(expense)), ("Balance", money(balance)), ("Transactions", str(len(transactions))), ("This Month Income", money(mi)), ("This Month Expense", money(me))]:
            grid.add_widget(Label(text=k))
            grid.add_widget(Label(text=v))
        root.add_widget(grid)
        actions = GridLayout(cols=2, size_hint_y=None, height=dp(150), spacing=dp(6))
        for text, target in [("+ Add Transaction", "add"), ("View Transactions", "transactions"), ("Accounts / Wallets", "accounts"), ("Currencies", "currency")]:
            b = Button(text=text)
            b.bind(on_release=lambda _, t=target: setattr(self.manager, "current", t))
            actions.add_widget(b)
        root.add_widget(actions)
        self.nav(root)
        self.clear_widgets(); self.add_widget(root)


class TransactionsScreen(BaseScreen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        root = self.root("Transactions")
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=dp(5), size_hint_y=None, padding=dp(4))
        grid.bind(minimum_height=grid.setter("height"))
        txs = list(reversed(self.app.common.transactions))
        if not txs:
            grid.add_widget(Label(text="No transactions yet.", size_hint_y=None, height=dp(50)))
        for t in txs:
            text = (f"{t.get('date','')}  |  {t.get('type','')}\n"
                    f"{t.get('category','')}  |  {t.get('original_amount', t.get('amount',0)):.2f} {t.get('currency','')}\n"
                    f"{t.get('account','')}  |  {t.get('description','')}")
            grid.add_widget(Label(text=text, size_hint_y=None, height=dp(78), halign="left", valign="middle"))
        scroll.add_widget(grid)
        root.add_widget(scroll)
        b = Button(text="+ Add Transaction", size_hint_y=None, height=dp(48))
        b.bind(on_release=lambda *_: setattr(self.manager, "current", "add"))
        root.add_widget(b)
        self.nav(root)
        self.clear_widgets(); self.add_widget(root)


class AddTransactionScreen(BaseScreen):
    def on_pre_enter(self, *args):
        self.build_form()

    def build_form(self):
        root = self.root("Add Transaction")
        self.kind = Spinner(text="Expense", values=("Expense", "Income"), size_hint_y=None, height=dp(48))
        self.account = Spinner(text=self.app.accounts.get_account_names()[0], values=tuple(self.app.accounts.get_account_names()), size_hint_y=None, height=dp(48))
        self.amount = TextInput(hint_text="Amount", input_filter="float", size_hint_y=None, height=dp(48))
        self.category = Spinner(text="Food", values=tuple(self.app.common.EXPENSE_CATEGORIES), size_hint_y=None, height=dp(48))
        self.description = TextInput(hint_text="Description", size_hint_y=None, height=dp(48))
        for w in [self.kind, self.account, self.amount, self.category, self.description]: root.add_widget(w)
        self.kind.bind(text=self.update_categories)
        save = Button(text="Save Transaction", size_hint_y=None, height=dp(52))
        save.bind(on_release=self.save)
        root.add_widget(save)
        back = Button(text="Back", size_hint_y=None, height=dp(48))
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "dashboard"))
        root.add_widget(back)
        self.clear_widgets(); self.add_widget(root)

    def update_categories(self, *_):
        self.category.values = tuple(self.app.common.EXPENSE_CATEGORIES if self.kind.text == "Expense" else self.app.common.INCOME_CATEGORIES)
        self.category.text = self.category.values[0]

    def save(self, *_):
        try:
            amount = float(self.amount.text)
            if amount <= 0: raise ValueError
            account = self.app.accounts.find_account(self.account.text)
            if not account: raise ValueError("Account not found")
            currency = str(account.get("currency", self.app.currency.get_base_currency())).upper()
            rate = self.app.currency.ensure_currency_rate(currency)
            base_amount, rate = self.app.currency.convert_to_base(amount, currency, rate)
            tx_id = f"TXN-{max([int(str(t.get('id','TXN-0000')).split('-')[-1]) for t in self.app.common.transactions if str(t.get('id','')).startswith('TXN-') and str(t.get('id','')).split('-')[-1].isdigit()] or [0]) + 1:04d}"
            self.app.common.transactions.append({"id": tx_id, "date": datetime.now().strftime("%d-%m-%Y"), "type": self.kind.text, "category": self.category.text, "amount": amount, "original_amount": amount, "currency": currency, "exchange_rate": rate, "base_amount": base_amount, "base_currency": self.app.currency.get_base_currency(), "account": self.account.text, "description": self.description.text.strip()})
            self.app.common.save_json(self.app.common.TRANSACTION_FILE, self.app.common.transactions)
            self.amount.text = ""; self.description.text = ""
            self.app.refresh(); self.manager.current = "dashboard"
            self.app.toast(f"Saved {tx_id}")
        except Exception as e:
            self.app.toast(f"Could not save transaction: {e}")


class AccountsScreen(BaseScreen):
    def on_pre_enter(self, *args): self.refresh()
    def refresh(self):
        root = self.root("Accounts / Wallets")
        scroll = ScrollView(); grid = GridLayout(cols=1, spacing=dp(5), size_hint_y=None); grid.bind(minimum_height=grid.setter("height"))
        for a in self.app.accounts.get_active_accounts():
            name = a.get("name", "")
            bal = self.app.accounts.account_balance_base(name)
            cur = str(a.get("currency", self.app.currency.get_base_currency())).upper()
            try: local = self.app.currency.convert_from_base(bal, cur) if cur != self.app.currency.get_base_currency() else bal
            except Exception: local = bal
            grid.add_widget(Label(text=f"{name}\n{a.get('type','Other')} • {cur}\nBalance: {local:.2f} {cur}", size_hint_y=None, height=dp(82)))
        scroll.add_widget(grid); root.add_widget(scroll)
        add = Button(text="Add Account", size_hint_y=None, height=dp(48)); add.bind(on_release=self.add_account); root.add_widget(add)
        self.nav(root); self.clear_widgets(); self.add_widget(root)

    def add_account(self, *_):
        content = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(8))
        name = TextInput(hint_text="Account name"); typ = Spinner(text="Cash", values=("Cash","Bank","eWallet","Card","Other")); cur = TextInput(text=self.app.currency.get_base_currency())
        ok = Button(text="Save", size_hint_y=None, height=dp(48))
        for w in [name, typ, cur, ok]: content.add_widget(w)
        pop = Popup(title="Add Account", content=content, size_hint=(.9,.6))
        def save(*_):
            n=name.text.strip(); c=cur.text.strip().upper()
            if n and c and not self.app.accounts.find_account(n):
                self.app.accounts.accounts.append({"name":n,"type":typ.text,"currency":c,"active":True}); self.app.accounts.save_accounts(); pop.dismiss(); self.app.refresh()
        ok.bind(on_release=save); pop.open()


class CurrencyScreen(BaseScreen):
    def on_pre_enter(self, *args): self.refresh()
    def refresh(self):
        root=self.root("Currency Settings")
        base=self.app.currency.get_base_currency()
        root.add_widget(Label(text=f"Base Currency: {base}", size_hint_y=None, height=dp(42)))
        scroll=ScrollView(); grid=GridLayout(cols=1, size_hint_y=None, spacing=dp(5)); grid.bind(minimum_height=grid.setter("height"))
        for code, rate in sorted(self.app.currency.get_rates().items()): grid.add_widget(Label(text=f"1 {base} = {rate:g} {code}", size_hint_y=None, height=dp(40)))
        scroll.add_widget(grid); root.add_widget(scroll)
        self.nav(root); self.clear_widgets(); self.add_widget(root)


if __name__ == "__main__":
    MoneyTrackerApp().run()
