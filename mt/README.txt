MONEY TRACKER - MODULAR VERSION
================================

This package keeps the Money Tracker features separated into modules:

- main.py             Application entry point
- menus.py            Main/transaction/report/loan menus
- transactions.py    Transaction add/edit/delete/search/filter/sort/PDF
- budgets.py         Monthly and category budgets
- loans.py           Lending/borrowing and repayments
- reports.py         Reports and PDF exports
- analytics.py       Dashboard and financial analysis
- common.py          Shared state, compatibility and helpers
- storage.py         Safe JSON save/load + backups + legacy migration
- config.py           Central file/folder configuration

IMPORTANT FIXES
---------------
1. All modules now use the centralized paths from config.py.
   Transactions are saved to data/transactions.json instead of an
   unrelated working-directory file.
2. datetime is explicitly imported in common.py because transaction,
   budget and analytics modules use it through `from common import *`.
3. Existing legacy root files can still be migrated automatically.
4. Existing transaction IDs/data compatibility is preserved.

TESTED
------
- All Python modules compile successfully.
- All modules import successfully.
- Add Transaction flow was executed successfully.
- Transaction was persisted to data/transactions.json.
- Generated transaction ID: TXN-0001 in a clean test.


Account deletion: Accounts/Wallets now includes permanent deletion. An account with linked transactions cannot be permanently deleted, protecting transaction history. Move transactions first, then delete.
