import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import re
import socket
from socket import *
import time
import os

clientSocket = None
server_address = None
registeredUser = None


def connect_to_server(input):
    global clientSocket, server_address

    pattern = r'^/join (\d+\.\d+\.\d+\.\d+) (\d+)$'
    match = re.match(pattern, input)

    if match and not clientSocket and not server_address:
        ip_address, port = match.groups()
        port = int(port)
        #print(ip_address)
        #print(port)
        server_address = (ip_address, port)
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        command = '/join'
        response_timeout = 2  # Timeout for waiting for a response from the server (in seconds)

        try:
            clientSocket.sendto(command.encode(), server_address) # Send command to server
            clientSocket.settimeout(response_timeout) # Timeout for receiving a response
            try:
                response, _ = clientSocket.recvfrom(2048)  # Buffer size is 2048 bytes
                response_message = response.decode()
                update_logs(f"{response_message}\n")
                #print(f"Response from server: {response_message}")
            
            except socket.timeout:
                # Handle timeout (no response received)
                update_logs("No response from server. Please check the server address and port.\n")
        
        except Exception as e:
            update_logs(f"Error: {e}\n")

    elif clientSocket and server_address:
        update_logs("Error: Already connected!\n")
    else:
        update_logs("Error: Connection to the Server has failed! Please check IP Address and Port Number.\n")

def disconnect_from_server():
    global clientSocket, server_address

    command = "/leave"
    if clientSocket and server_address:
        try:
            # Send the disconnect command to the server
            clientSocket.sendto(command.encode(), server_address)
            
            # Print the details to confirm
            update_logs(f"Sending command: {command}\n")
        
        except Exception as e:
            # Handle errors
            #print(f"Error: {e}")
            update_logs(f"Error: {e}\n")
        
        finally:
            # Close the socket
            clientSocket.close()
            clientSocket = None
            server_address = None
            registeredUser = False

            update_logs("Connection closed. Thank you!\n")
    else:
        update_logs("Error: Disconnection failed. Please connect to the server first.\n")


def register_handle(input):
    global clientSocket, server_address, registeredUser

    if clientSocket and server_address and not registeredUser:
        clientSocket.sendto(input.encode(), server_address)
        response, _ = clientSocket.recvfrom(2048)
        response_message = response.decode()
        update_logs(f"{response_message}\n")

        if "registered successfully" in response_message:
            registeredUser = True

    elif registeredUser:
        update_logs("Error: Already a registered user!\n")
    else:
        update_logs("Error: Not connected to a server. Please connect to the server first.\n")


def store_file(input):
    global clientSocket, server_address, registeredUser

    if clientSocket and server_address and registeredUser:
        if len(input.split()) == 2:
            filename = input.split(' ')[1]  # Extract the filename from the command input
            file_path = f"./Client Files/{filename}"
            
            try:
                with open(file_path, 'rb') as f:
                    command = f"/store {filename}"
                    clientSocket.sendto(command.encode(), server_address)

                    # Wait for the server to be ready
                    response, _ = clientSocket.recvfrom(2048)
                    response_message = response.decode()
                    update_logs(f"{response_message}\n")

                    if "Ready to receive" in response_message:
                        while True:
                            chunk = f.read(1024)

                            #print(f"inner chunk: {chunk}\n")
                            if chunk:
                                clientSocket.sendto(chunk, server_address)
                            else:
                                break
                        clientSocket.sendto(b'EOF', server_address)  # Send end of file marker

                        time.sleep(1)

                        response, _ = clientSocket.recvfrom(2048)
                        response_message = response.decode()
                        update_logs(f"{response_message}\n")
            
            except FileNotFoundError:
                update_logs("File does not exist.\n")
        
            except Exception as e:
                update_logs(f"Error: {e}\n")

        else:
            update_logs("Invalid store command. Usage: /store <filename>\n")

    elif clientSocket and server_address:
        update_logs("Error: Not registered to the server. Please register first.\n")
    else:
        update_logs("Error: Not connected to a server. Please connect to the server first.\n")


def get_file(input):
    global clientSocket, server_address, registeredUser

    if clientSocket and server_address and registeredUser:
        if len(input.split()) == 2:
            filename = input.split(' ')[1]  # Extract the filename from the command input
            command = f"/get {filename}"
            clientSocket.sendto(command.encode(), server_address)

            try:
                response, _ = clientSocket.recvfrom(2048)
                response_message = response.decode()
                update_logs(f"{response_message}\n")

                if "Ready to send file" in response_message:
                    file_path = f"./Client Files/{filename}"
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    file_data = b''
                    with open(file_path, 'wb') as f:
                        while True:
                            chunk, _ = clientSocket.recvfrom(2048)

                            if chunk == b'EOF':
                                f.write(file_data)
                                response, _ = clientSocket.recvfrom(2048)
                                response_message = response.decode()
                                update_logs(f"{response_message}\n")
                                break
                            else:
                                file_data += chunk
            
            except Exception as e:
                update_logs(f"Error in get_file function: {e}\n")
        else:
            update_logs("Invalid get command. Usage: /get <filename>\n")

    elif clientSocket and server_address:
        update_logs("Error: Not registered to the server. Please register first.\n")
    else:
        update_logs("Error: Not connected to a server. Please connect to the server first.\n")


def request_dir():
    global clientSocket, server_address, registeredUser

    if clientSocket and server_address and registeredUser:
        command = "/dir"
        clientSocket.sendto(command.encode(), server_address)
        
        try:
            response, _ = clientSocket.recvfrom(2048)
            response_message = response.decode()
            update_logs(f"{response_message}\n")
        except Exception as e:
            update_logs(f"Error: {e}\n")

    elif clientSocket and server_address:
        update_logs("Error: Not registered to the server. Please register first.\n")
    else:
        update_logs("Error: Not connected to a server. Please connect to the server first.\n")


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
    update_logs(f"Help:\n{help_text}\n")

def execute_command():
    input_text = send_entry.get()
    send_entry.delete(0, tk.END)
    
    if '/join' in input_text:
        connect_to_server(input_text)

    elif '/leave' in input_text:
        disconnect_from_server()

    elif '/register' in input_text:
        register_handle(input_text)

    elif '/store' in input_text:
        store_file(input_text)

    elif '/dir' in input_text:
        request_dir()

    elif '/get' in input_text:
        get_file(input_text)

    elif '/?' in input_text:
        show_help()

    else:
        update_logs("Unknown command\n")

def update_logs(text):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, time.strftime("%H:%M:%S") + ": ")
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)


# ========================= GUI ========================= #
# Create the main windoww
main_window = tk.Tk()
main_window.title("CSNETWK MCO - Client Interface")
window_width = 600
window_height = 350

# Get the screen dimensions
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

# Calculate the position for the window to be centered
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the size and position of the main window
main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

widget_width = 60

command_label = tk.Label(main_window, text="Command:")
command_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

# Command text field
send_entry = tk.Entry(main_window, width=widget_width)
send_entry.grid(row=0, column=1, padx=10, pady=10)

logs_label = tk.Label(main_window, text="Logs:")
logs_label.grid(row=1, column=0, padx=10, pady=10, sticky="ne")

# Output logs
output_text = scrolledtext.ScrolledText(main_window, wrap=tk.WORD, height=15, width=widget_width, state=tk.DISABLED)
output_text.grid(row=1, column=1, padx=10, pady=10)

# Frame for the buttons
button_frame = tk.Frame(main_window)
button_frame.grid(row=2, column=1, pady=10)

send_button = tk.Button(button_frame, text="Send", command=execute_command, font=("Arial", 12), width=15, height=2)
send_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(button_frame, text="Exit", command=main_window.quit, bg="red", fg="white", font=("Arial", 12), width=15, height=2)
exit_button.pack(side=tk.LEFT, padx=5)

# Run the Tkinter event loop
main_window.mainloop()
