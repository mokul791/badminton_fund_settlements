Badminton Expense Splitter
=============================
A simple, modern, minimal tool to fairly split shared badminton facility expenses.


Overview
------------
Badminton Expense Splitter helps you and your friends record how much each person paid toward court booking or related expenses—and instantly calculates the minimal number of transfers needed to settle up fairly.

Just enter:

The number of players

Each player’s name

How much each person paid

The app calculates:

Total amount spent

Fair share per person

Individual contributions

A concise list of “Who pays whom” with minimal transactions

Clean, fast, and designed for real-world group play sessions.


Features
-------------
Modern minimal GUI (Tkinter-based)

Input any number of players

Auto-generated player rows

Robust validation (names, amounts, negative values, etc.)

Computes settlements with minimal money transfers

Real-time results displayed in a clean text panel

Reset button to start a fresh calculation instantly

Embedded branding footer

Lightweight macOS .app bundle (packaged with PyInstaller)

Works fully offline


Installation (macOS)
------------------------
Option 1: Use the pre-built app

If you received the .app bundle:

Unzip the file if needed

Move Badminton Expense Splitter.app to your Applications folder

Right-click -> Open (first time only)

From then on, double-click normally

macOS may warn you about running apps from unidentified developers.
Use Right-click -> Open to bypass this safely.

Building the app from source (for developers)
-----------------------------------------------
Requirements

macOS

Python 3.11.x (recommended from python.org)

PyInstaller inside a virtual environment

Clone or copy the project
git clone <your-repo-url>
cd badminton-expense-splitter

Create and activate a venv
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

Install PyInstaller
pip install pyinstaller

Build the macOS .app
pyinstaller \
  --windowed \
  --name "Badminton Expense Splitter" \
  --icon app_icon.icns \
  --add-data "badminton_logo.png:." \
  badminton_splitter_modern.py


The app will be created at:

dist/Badminton Expense Splitter.app

Project Structure
-----------------------
badminton_expense_splitter/
│
├── badminton_splitter_modern.py   # Main application code
├── badminton_logo.png             # Header logo used in UI
├── app_icon.icns                  # macOS app icon
├── README.md
└── ... (PyInstaller build folders added automatically)

How the Settlement Algorithm Works
--------------------------------------
The algorithm computes:

Total spent by all players

Fair share = total / number of players

For each person:

If they paid more → creditor

If they paid less → debtor

Then it walks the creditor/debtor lists and generates minimal required transfers so everyone ends up paying exactly their fair share.

Example:

Person	Paid
Ismail	30
Alice	45
Bob	60

Total = 135

Fair share = 45

Output might be:

Ismail pays Bob 15

Only one transaction needed.

Credits
----------------------

Developed by:
Ismail
© 2025 — All Rights Reserved

Feedback / Suggestions
-----------------------

If you have feature requests or ideas to improve the UI/UX, feel free to reach out or open an issue in the repository.