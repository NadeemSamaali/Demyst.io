import tkinter as tk
from tkinter import scrolledtext
from chatbot import run_chatbot

# Function to handle sending messages
def send_message():
    user_message = user_input.get()
    if user_message.strip():
        chat_display.insert(tk.END, "# " + user_message + "\n")
        bot_response = run_chatbot(user_message)
        chat_display.insert(tk.END, bot_response + "\n")
        user_input.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Chatbot")

# Create a scrolled text widget for displaying messages
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create an entry widget for typing messages
user_input = tk.Entry(root)
user_input.pack(padx=10, pady=10, fill=tk.X)

# Create a send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

root.mainloop()
