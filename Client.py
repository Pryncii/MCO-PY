import tkinter as tk

def submit():
    user_input = entry.get()
    print("User Input:", user_input)

def button_click():
    print("Button was clicked!")
    entry.pack(pady=10)
    submit_button = tk.Button(main_window, text="Submit", command=submit)
    submit_button.pack(pady=5)


# Create the main windoww
main_window = tk.Tk()
main_window.title("CSNETWK MCO")
window_width = 300
window_height = 200

# Get the screen dimensions
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

# Calculate the position for the window to be centered
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the size and position of the main window
main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a Button widget
start_button = tk.Button(main_window, text="Start", command=button_click, width=15, height=2)
start_button.pack(pady=5)

# Add the text entry
entry = tk.Entry(main_window, width=30)

# Create another Button with different options
exit_button = tk.Button(main_window, text="Exit", command=main_window.quit, bg="red", fg="white", font=("Arial", 12))
exit_button.pack(pady=10)

# Run the Tkinter event loop
main_window.mainloop()
