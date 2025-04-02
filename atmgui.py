import tkinter as tk
from tkinter import simpledialog, messagebox

# Initial account setup
originalpin=1234
balance=5000
transactionhistory = []

# Function to display the main menu
def display_menu():
    menu_label.config(text="""
    1 == Balance
    2 == Withdraw Amount
    3 == Deposit Amount
    4 == PIN Change
    5 == Transaction History
    6 == Exit
    """)
    menu_frame.pack(pady=20)

# Function to check PIN
def check_pin():
    global originalpin
    pin = simpledialog.askinteger("PIN Entry", "Enter the ATM PIN:")
    if pin == originalpin:
        display_menu()
    else:
        messagebox.showerror("Error", "Wrong PIN. Please try again.")
        root.quit()

# Function to handle the user's choice
def handle_choice():
    global balance
    try:
        option = int(entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid option.")
        return

    if option == 1:  # Balance Inquiry
        messagebox.showinfo("Balance Inquiry", f"Your current balance is {balance}")
        transactionhistory.append(f"Balance Inquiry: {balance}")

    elif option == 2:  # Cash Withdrawal
        withdraw_amount = simpledialog.askinteger("Withdrawal", "Please enter withdrawal amount:")
        if withdraw_amount and withdraw_amount <= balance:
            balance -= withdraw_amount
            messagebox.showinfo("Withdrawal", f"{withdraw_amount} has been withdrawn from your account.")
            transactionhistory.append(f"Withdrawal: {withdraw_amount}")
        else:
            messagebox.showerror("Error", "Insufficient balance or invalid amount.")

    elif option == 3:  # Cash Deposit
        deposit_amount = simpledialog.askinteger("Deposit", "Please enter deposit amount:")
        if deposit_amount:
            balance += deposit_amount
            messagebox.showinfo("Deposit", f"{deposit_amount} has been deposited into your account.")
            transactionhistory.append(f"Deposit: {deposit_amount}")

    elif option == 4:  # PIN Change
        new_pin = simpledialog.askinteger("PIN Change", "Enter your new PIN:", show='*')
        confirm_pin = simpledialog.askinteger("PIN Change", "Confirm your new PIN:", show='*')
        if new_pin == confirm_pin:
            originalpin = new_pin
            messagebox.showinfo("PIN Change", "PIN changed successfully.")
            transactionhistory.append("PIN Change")
        else:
            messagebox.showerror("Error", "PINs do not match. Please try again.")

    elif option == 5:  # Transaction History
        if transactionhistory:
            history = "\n".join(transactionhistory)
            messagebox.showinfo("Transaction History", history)
        else:
            messagebox.showinfo("Transaction History", "No transactions yet.")

    elif option == 6:  # Exit
        messagebox.showinfo("Exit", "Thank you for using our ATM.")
        root.quit()

    else:
        messagebox.showerror("Error", "Invalid option. Please try again.")

# Create the main window
root = tk.Tk()
root.title("ATM Machine Simulation")
root.geometry("500x500")

# Welcome label
welcome_label = tk.Label(root, text="Welcome to the ATM", font=("Times New Roman", 16))
welcome_label.pack(pady=10)

# Insert card label
insert_card_label = tk.Label(root, text="Please insert your card...", font=("Times New Roman", 14))
insert_card_label.pack(pady=5)

# Menu frame
menu_frame = tk.Frame(root)
menu_label = tk.Label(menu_frame, text="", font=("Times New Roman", 12))
menu_label.pack()

# Entry for option
entry = tk.Entry(root)
entry.pack(pady=10)

# Button to confirm choice
confirm_button = tk.Button(root, text="Confirm", command=handle_choice)
confirm_button.pack(pady=10)

# Start the PIN check
root.after(2000, check_pin)  # Simulate card insertion delay
root.mainloop()
