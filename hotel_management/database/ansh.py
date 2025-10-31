import tkinter as tk
from tkinter import messagebox

# Function to handle submit button
def submit_form():
    name = name_entry.get()
    uid = uid_entry.get()
    messagebox.showinfo("Registration", f"Name: {name}\nUID: {uid}\nRegistration Successful!")

# Function to handle exit button
def exit_app():
    window.destroy()

# Create main window
window = tk.Tk()
window.title("Registration Form")
window.geometry("350x250")
window.configure(bg="Light grey")

# Heading
heading = tk.Label(window, text="Student Registration Form", font=("Arial", 14, "bold"), bg="Light grey")
heading.pack(pady=10)

# Name label and entry
tk.Label(window, text="Name:", font=("Arial", 12), bg="Light grey").pack()
name_entry = tk.Entry(window, width=30)
name_entry.pack(pady=5)
name_entry.insert(0, "Ansh Soni")

# UID label and entry
tk.Label(window, text="UID:", font=("Arial", 12), bg="Light grey").pack()
uid_entry = tk.Entry(window, width=30)
uid_entry.pack(pady=5)
uid_entry.insert(0, "25MCD10026")

# Buttons (Process control)
submit_btn = tk.Button(window, text="Submit", bg="light green", fg="white", width=10, command=submit_form)
submit_btn.pack(pady=10)

exit_btn = tk.Button(window, text="Exit", bg="red", fg="white", width=10, command=exit_app)
exit_btn.pack()

# Run the Tkinter event loop
window.mainloop()