import os
import sys
import tkinter as tk
from tkinter import messagebox

# -------------------------
# Modern Minimal Palette
# -------------------------
PALETTE = {
    "bg": "#F5F5F7",
    "card": "#FFFFFF",
    "primary": "#2563EB",          # Blue
    "primary_hover": "#1E40AF",    # Darker Blue (for other uses if needed)
    "text_main": "#111827",
    "text_muted": "#6B7280",
    "border": "#E5E7EB",
}

person_rows = []  # will hold (name_entry, amount_entry) tuples


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to a resource.

    Works for:
    - Running from source
    - PyInstaller bundle (sys._MEIPASS)
    - py2app bundle (sys.frozen with Resources dir)
    """
    # PyInstaller: resources are unpacked into a temp folder at runtime
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)

    # py2app or other frozen modes
    if getattr(sys, "frozen", False):
        # Executable is in .../YourApp.app/Contents/MacOS/
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        # Resources are in .../YourApp.app/Contents/Resources/
        resources_path = os.path.normpath(os.path.join(base_path, "..", "Resources"))
        return os.path.join(resources_path, relative_path)

    # Running from source .py file
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def compute_settlements(payments):
    """
    Given a dict {name: amount_paid}, compute minimal settlement transactions.
    Returns a list of strings like "Ismail pays Bob 15.00".
    """
    names = list(payments.keys())
    n = len(names)
    total = sum(payments.values())
    if n == 0:
        return ["No players found."]

    fair_share = total / n

    creditors = []  # [ [name, amount_to_receive], ... ]
    debtors = []    # [ [name, amount_to_pay], ... ]

    for name, paid in payments.items():
        net = round(paid - fair_share, 2)
        if net > 0:
            creditors.append([name, net])
        elif net < 0:
            debtors.append([name, -net])

    if not creditors and not debtors:
        return ["Everyone is already settled."]

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    settlements = []
    i = j = 0

    while i < len(debtors) and j < len(creditors):
        debtor_name, debtor_amt = debtors[i]
        creditor_name, creditor_amt = creditors[j]

        x = round(min(debtor_amt, creditor_amt), 2)
        if x > 0:
            settlements.append(f"{debtor_name} pays {creditor_name} {x:.2f}")

        debtors[i][1] = round(debtor_amt - x, 2)
        creditors[j][1] = round(creditor_amt - x, 2)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return settlements


def build_person_rows():
    """
    Create input rows for each player based on the number entered.
    """
    global person_rows
    person_rows = []

    # Clear previous rows
    for widget in people_frame.winfo_children():
        widget.destroy()

    num_str = num_people_entry.get().strip()
    if not num_str:
        messagebox.showerror("Input Error", "Please enter number of players.")
        return

    try:
        num = int(num_str)
    except ValueError:
        messagebox.showerror("Input Error", "Number of players must be an integer.")
        return

    if num <= 0:
        messagebox.showerror("Input Error", "Number of players must be at least 1.")
        return

    header_font = ("Segoe UI", 10, "bold")

    tk.Label(
        people_frame,
        text="Player",
        bg=PALETTE["card"],
        fg=PALETTE["text_muted"],
        font=header_font,
    ).grid(row=0, column=0, padx=8, pady=6, sticky="w")
    tk.Label(
        people_frame,
        text="Name",
        bg=PALETTE["card"],
        fg=PALETTE["text_muted"],
        font=header_font,
    ).grid(row=0, column=1, padx=8, pady=6, sticky="w")
    tk.Label(
        people_frame,
        text="Amount Paid",
        bg=PALETTE["card"],
        fg=PALETTE["text_muted"],
        font=header_font,
    ).grid(row=0, column=2, padx=8, pady=6, sticky="w")

    for i in range(num):
        row_index = i + 1
        tk.Label(
            people_frame,
            text=f"{row_index}",
            bg=PALETTE["card"],
            fg=PALETTE["text_muted"],
            font=("Segoe UI", 10),
        ).grid(row=row_index, column=0, padx=8, pady=4, sticky="w")

        name_entry = tk.Entry(
            people_frame,
            width=20,
            bg="#F9FAFB",
            fg=PALETTE["text_main"],
            borderwidth=1,
            relief="solid",
            highlightthickness=0,
        )
        name_entry.grid(row=row_index, column=1, padx=8, pady=4, sticky="we")

        amount_entry = tk.Entry(
            people_frame,
            width=12,
            bg="#F9FAFB",
            fg=PALETTE["text_main"],
            borderwidth=1,
            relief="solid",
            highlightthickness=0,
        )
        amount_entry.grid(row=row_index, column=2, padx=8, pady=4, sticky="we")

        person_rows.append((name_entry, amount_entry))

    people_frame.grid_columnconfigure(1, weight=1)


def on_calculate():
    """
    Read entered data, validate, compute settlements, and show results.
    """
    if not person_rows:
        messagebox.showerror("Input Error", "Please create player rows first.")
        return

    payments = {}
    for i, (name_entry, amount_entry) in enumerate(person_rows, start=1):
        name = name_entry.get().strip()
        amount_str = amount_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", f"Player {i}: Name is required.")
            return

        if not amount_str:
            messagebox.showerror("Input Error", f"Player {i} ({name}): Amount is required.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror(
                "Input Error",
                f"Player {i} ({name}): Amount must be a valid number."
            )
            return

        if amount < 0:
            messagebox.showerror(
                "Input Error",
                f"Player {i} ({name}): Amount cannot be negative."
            )
            return

        payments[name] = payments.get(name, 0) + amount

    settlements = compute_settlements(payments)

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)

    total = sum(payments.values())
    n = len(payments)
    fair_share = total / n

    output_text.insert(tk.END, f"Total spent: {total:.2f}\n")
    output_text.insert(tk.END, f"Players: {n}\n")
    output_text.insert(tk.END, f"Fair share per person: {fair_share:.2f}\n\n")

    output_text.insert(tk.END, "Individual totals:\n")
    for name, amt in payments.items():
        output_text.insert(tk.END, f"  {name}: {amt:.2f}\n")

    output_text.insert(tk.END, "\nSettlements (who pays whom):\n")
    for line in settlements:
        output_text.insert(tk.END, f"  • {line}\n")

    output_text.config(state=tk.DISABLED)


def on_reset():
    """
    Reset the entire app to initial state for a new calculation.
    """
    global person_rows
    # Clear player rows
    for widget in people_frame.winfo_children():
        widget.destroy()
    person_rows = []

    # Clear number of players entry
    num_people_entry.delete(0, tk.END)

    # Clear output
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)


# -------------------------
# GUI Setup (Modern Minimal)
# -------------------------

root = tk.Tk()
root.title("Badminton Expense Splitter")

# Overall background
root.configure(bg=PALETTE["bg"])
root.minsize(550, 450)

# --- Top bar / header ---
top_bar = tk.Frame(root, bg=PALETTE["bg"])
top_bar.pack(fill="x", padx=16, pady=(12, 0))

app_title = tk.Label(
    top_bar,
    text="Badminton Expense Splitter",
    bg=PALETTE["bg"],
    fg=PALETTE["text_main"],
    font=("Segoe UI", 15, "bold"),
)
app_title.pack(side="left", anchor="w")

subtitle = tk.Label(
    top_bar,
    text="Fair, simple settlements with minimal transfers",
    bg=PALETTE["bg"],
    fg=PALETTE["text_muted"],
    font=("Segoe UI", 10),
)
subtitle.pack(side="left", padx=(10, 0), anchor="w")

# --- Logo on the right side of the header ---
try:
    logo_path = resource_path("badminton_logo.png")
    root.logo_img = tk.PhotoImage(file=logo_path)
    # scale down as you like; 8,8 makes it quite small
    root.logo_img = root.logo_img.subsample(8, 8)
    logo_label = tk.Label(top_bar, image=root.logo_img, bg=PALETTE["bg"])
    logo_label.pack(side="right")
except Exception as e:
    print("Logo not loaded:", e)

# --- Card container ---
card = tk.Frame(
    root,
    bg=PALETTE["card"],
    bd=1,
    relief="solid",
    highlightthickness=0,
)
card.pack(fill="both", expand=True, padx=16, pady=10)

# --- Number input row ---
top_frame = tk.Frame(card, bg=PALETTE["card"])
top_frame.pack(padx=12, pady=12, fill="x")

tk.Label(
    top_frame,
    text="Number of players",
    bg=PALETTE["card"],
    fg=PALETTE["text_main"],
    font=("Segoe UI", 10),
).pack(side="left")

num_people_entry = tk.Entry(
    top_frame,
    width=6,
    bg="#F9FAFB",
    fg=PALETTE["text_main"],
    borderwidth=1,
    relief="solid",
    highlightthickness=0,
)
num_people_entry.pack(side="left", padx=8)


# --- Hover handlers for buttons ---
def on_enter_build(e):
    build_button.config(bg="#E0ECFF")


def on_leave_build(e):
    build_button.config(bg="white")


def on_enter_calc(e):
    calc_button.config(bg="#E0ECFF")


def on_leave_calc(e):
    calc_button.config(bg="white")


def on_enter_reset(e):
    reset_button.config(bg="#9CA3AF")  # slightly darker grey


def on_leave_reset(e):
    reset_button.config(bg="#D1D5DB")  # lighter grey


# --- Create Player Rows button (blue text) ---
build_button = tk.Button(
    top_frame,
    text="Create Player Rows",
    command=build_person_rows,
    bg="white",
    fg=PALETTE["primary"],              # blue text
    activeforeground=PALETTE["primary"],
    activebackground="#E0ECFF",
    relief="solid",
    borderwidth=1,
    padx=10,
    pady=4,
    font=("Segoe UI", 9, "bold"),
    cursor="hand2",
)
build_button.pack(side="left", padx=8)
build_button.bind("<Enter>", on_enter_build)
build_button.bind("<Leave>", on_leave_build)

# --- Player rows area ---
people_frame = tk.Frame(card, bg=PALETTE["card"])
people_frame.pack(padx=12, pady=(0, 10), fill="x")

# --- Bottom controls (Calculate + Reset) ---
bottom_controls = tk.Frame(card, bg=PALETTE["card"])
bottom_controls.pack(padx=12, pady=(0, 10), fill="x")

# Reset button (left)
reset_button = tk.Button(
    bottom_controls,
    text="Reset",
    command=on_reset,
    bg="#D1D5DB",
    fg=PALETTE["text_main"],
    activeforeground=PALETTE["text_main"],
    activebackground="#9CA3AF",
    relief="flat",
    padx=12,
    pady=6,
    font=("Segoe UI", 10, "bold"),
    cursor="hand2",
)
reset_button.pack(side="left")
reset_button.bind("<Enter>", on_enter_reset)
reset_button.bind("<Leave>", on_leave_reset)

# Calculate button (right, blue text)
calc_button = tk.Button(
    bottom_controls,
    text="Calculate Settlements",
    command=on_calculate,
    bg="white",
    fg=PALETTE["primary"],              # blue text
    activeforeground=PALETTE["primary"],
    activebackground="#E0ECFF",
    relief="solid",
    borderwidth=1,
    padx=12,
    pady=6,
    font=("Segoe UI", 10, "bold"),
    cursor="hand2",
)
calc_button.pack(side="right")
calc_button.bind("<Enter>", on_enter_calc)
calc_button.bind("<Leave>", on_leave_calc)

# --- Output area ---
output_label = tk.Label(
    card,
    text="Result",
    bg=PALETTE["card"],
    fg=PALETTE["text_main"],
    font=("Segoe UI", 10, "bold"),
)
output_label.pack(padx=12, anchor="w", pady=(0, 2))

output_text = tk.Text(
    card,
    width=60,
    height=12,
    state=tk.DISABLED,
    bg="#F9FAFB",
    fg=PALETTE["text_main"],
    borderwidth=1,
    relief="solid",
    highlightthickness=0,
    font=("Consolas", 9),
)
output_text.pack(padx=12, pady=(0, 12), fill="both", expand=True)

# --- Branding Footer ---
branding = tk.Label(
    root,
    text="© 2025 Ismail — All Rights Reserved",
    font=("Segoe UI", 9),
    fg=PALETTE["text_muted"],
    bg=PALETTE["bg"],
    pady=6,
)
branding.pack(side="bottom", fill="x")

root.mainloop()
