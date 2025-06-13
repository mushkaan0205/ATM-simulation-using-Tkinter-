import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from reportlab.pdfgen import canvas
import pyttsx3
import matplotlib.pyplot as plt
import os

# === Voice Assistant Setup ===
def speak(text):
    import threading
    def run_speech():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech).start()

# === Dummy Users ===
users = {
    "Rajesh Malhotra": {"pin": 1234, "balance": 5000, "history": [], "deposits": 0, "withdrawals": 0},
    "Mushkaan Mohanta": {"pin": 4321, "balance": 3000, "history": [], "deposits": 0, "withdrawals": 0},
    "Suhani Singh": {"pin": 1111, "balance": 10000, "history": [], "deposits": 0, "withdrawals": 0},
}

current_user = None

# === Function Definitions ===
def select_user():
    global current_user
    username = user_select.get()
    current_user = users[username]
    speak("Proceeding to PIN verification")
    check_pin()

def check_pin():
    pin = simpledialog.askinteger("PIN", "Enter your PIN:")
    if pin == current_user["pin"]:
        speak("PIN verified successfully")
        show_dashboard()
    else:
        speak("Incorrect PIN")
        messagebox.showerror("Access Denied", "Wrong PIN")
        root.quit()

def show_dashboard():
    login_frame.pack_forget()
    dashboard_frame.pack(fill='both', expand=True)
    update_balance()
    update_history()

def withdraw_amount():
    amt = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
    if amt and amt <= current_user["balance"]:
        current_user["balance"] -= amt
        current_user["withdrawals"] += amt
        current_user["history"].append(f"Withdrew ₹{amt}")
        update_balance()
        update_history()
        speak(f"₹{amt} withdrawn successfully")
    else:
        speak("Insufficient balance or invalid input")
        messagebox.showerror("Error", "Insufficient balance or invalid amount")

def deposit_amount():
    amt = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
    if amt:
        current_user["balance"] += amt
        current_user["deposits"] += amt
        current_user["history"].append(f"Deposited ₹{amt}")
        update_balance()
        update_history()
        speak(f"₹{amt} deposited successfully")

def change_pin():
    new = simpledialog.askinteger("New PIN", "Enter new PIN:")
    confirm = simpledialog.askinteger("Confirm", "Re-enter new PIN:")
    if new == confirm:
        current_user["pin"] = new
        current_user["history"].append("PIN changed")
        speak("PIN changed successfully")
        messagebox.showinfo("Success", "PIN changed.")
    else:
        speak("PINs do not match")
        messagebox.showerror("Error", "PINs did not match.")

def download_pdf():
    if not current_user["history"]:
        speak("No transaction to download")
        messagebox.showinfo("Empty", "No transactions yet.")
        return

    folder = filedialog.askdirectory()
    if not folder: return

    filepath = os.path.join(folder, "ATM_Statement.pdf")
    c = canvas.Canvas(filepath)
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, "ATM Transaction Statement")
    c.setFont("Helvetica", 12)
    y = 770
    for item in current_user["history"]:
        c.drawString(50, y, f"• {item}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    speak("Statement saved as PDF")
    messagebox.showinfo("Downloaded", f"PDF saved: {filepath}")

def show_graph():
    if current_user["deposits"] == 0 and current_user["withdrawals"] == 0:
        speak("No data to display")
        messagebox.showinfo("No Data", "No deposits or withdrawals yet.")
        return

    labels = ['Deposits', 'Withdrawals']
    values = [current_user["deposits"], current_user["withdrawals"]]

    plt.figure(figsize=(6, 4))
    plt.subplot(121)
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Spending Overview')

    plt.subplot(122)
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
    plt.title('Spending Ratio')

    plt.tight_layout()
    plt.show()

def update_balance():
    balance_label.config(text=f"₹{current_user['balance']}")

def update_history():
    for w in history_frame.winfo_children():
        w.destroy()
    if not current_user["history"]:
        tk.Label(history_frame, text="No recent transactions.", bg="#ecf0f1").pack()
    else:
        for h in current_user["history"][-5:][::-1]:
            tk.Label(history_frame, text=f"• {h}", bg="#ecf0f1", anchor='w').pack(fill='x')

def chatbot_assist():
    messagebox.showinfo("ChatBot", "Hi! I'm your ATM assistant.\n\nNeed help?\n- Withdraw/Deposit\n- Check balance\n- Download statement\n- Contact support")

# === GUI Setup ===
root = tk.Tk()
root.title("Smart ATM Dashboard")
root.geometry("750x600")
root.configure(bg="white")

# === Login Frame ===
login_frame = tk.Frame(root, bg="white")
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="🔐 Select Your Card", font=("Helvetica", 18, "bold"), bg="white").pack(pady=20)

user_select = ttk.Combobox(login_frame, values=list(users.keys()), font=("Helvetica", 14), state="readonly", width=20)
user_select.set("Choose a card")
user_select.pack(pady=10)

tk.Button(login_frame, text="Proceed", font=("Helvetica", 14), bg="#2ecc71", fg="white", command=select_user).pack(pady=20)

# === Dashboard Frame ===
dashboard_frame = tk.Frame(root, bg="white")

navbar = tk.Frame(dashboard_frame, bg="#34495e")
navbar.pack(fill='x')

for txt, func in [("Withdraw", withdraw_amount), ("Deposit", deposit_amount), ("Change PIN", change_pin),
                  ("PDF", download_pdf), ("Graph", show_graph), ("ChatBot", chatbot_assist), ("Exit", root.quit)]:
    tk.Button(navbar, text=txt, command=func, bg="#1abc9c", fg="white", padx=10, pady=5).pack(side="left", padx=6, pady=8)

balance_card = tk.Frame(dashboard_frame, bg="#dff9fb", height=60, bd=1, relief='solid')
balance_card.pack(fill='x', padx=20, pady=10)
tk.Label(balance_card, text="💰 Balance", font=("Helvetica", 14, "bold"), bg="#dff9fb").pack(anchor='w', padx=10)
balance_label = tk.Label(balance_card, text="", font=("Helvetica", 12), bg="#dff9fb")
balance_label.pack(anchor='w', padx=20)

history_frame = tk.Frame(dashboard_frame, bg="#ecf0f1", bd=1, relief="sunken")
history_frame.pack(fill='both', expand=True, padx=20, pady=10)
tk.Label(history_frame, text="📄 Last Transactions", font=("Helvetica", 12, "bold"), bg="#ecf0f1").pack(anchor='w', padx=10, pady=5)

root.mainloop()

