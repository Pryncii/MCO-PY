import tkinter as tk
from tkinter import scrolledtext


def connect_to_server():
    command = f"/join"
    output_text.insert(tk.END, f"Sending command: {command}\n")

def disconnect_from_server():
    command = "/leave"
    output_text.insert(tk.END, f"Sending command: {command}\n")

def register_handle():
    command = f"/register"
    output_text.insert(tk.END, f"Sending command: {command}\n")


def store_file():
    command = f"/store"
    output_text.insert(tk.END, f"Sending command: {command}\n")


def get_file():
    command = f"/get"
    output_text.insert(tk.END, f"Sending command: {command}\n")


def request_dir():
    command = "/dir"
    output_text.insert(tk.END, f"Sending command: {command}\n")

def show_help():
    help_text = (
        "/join <server_ip_add> <port>\n"
        "/leave\n"
        "/register <handle>\n"
        "/store <filename>\n"
        "/dir\n"
        "/get <filename>\n"
        "/?\n"
    )
    output_text.insert(tk.END, f"Help:\n{help_text}\n")

def execute_command():
    input_text = send_entry.get()
    
    if '/join' in input_text:
        connect_to_server()
    elif '/leave' in input_text:
        disconnect_from_server()
    elif '/register' in input_text:
        register_handle()
    elif '/store' in input_text:
        store_file()
    elif '/dir' in input_text:
        request_dir()
    elif '/get' in input_text:
        get_file()
    elif '/?' in input_text:
        show_help()
    else:
        output_text.insert(tk.END, "Unknown command\n")



# Create the main windoww
main_window = tk.Tk()
main_window.title("CSNETWK MCO")
window_width = 600
window_height = 400

# Get the screen dimensions
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

# Calculate the position for the window to be centered
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the size and position of the main window
main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


# Create a Button widget
# Add the text entry
send_entry = tk.Entry(main_window, width=30)
send_entry.pack(pady=10)
input = send_entry.get()


send_button = tk.Button(main_window, text="Send", command = execute_command, width=15, height=2)
send_button.pack(pady=10)


# Create another Button with different options
exit_button = tk.Button(main_window, text="Exit", command=main_window.quit, bg="red", fg="white", font=("Arial", 12))
exit_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(main_window, wrap=tk.WORD, height=40, width=60)
output_text.pack(pady=10)

# Run the Tkinter event loop
main_window.mainloop()
