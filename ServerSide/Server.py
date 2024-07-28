from socket import *
import threading

# Define server port and create UDP socket
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('Server: The server is ready to receive')
clients = {}

def handle_client_message(message, client_address):
    global clients

    command_parts = message.strip().split()
    command = command_parts[0]

    if command == '/join':
        response = f"Welcome! Your address is {client_address}"
    
    elif command == '/leave':
        print("wip")
    
    elif command == '/register':
        if len(command_parts) == 2:
            handle = command_parts[1]

            if handle in clients.values():
                response = f"Error: Handle '{handle}' is already in use."
            
            else:
                clients[client_address] = handle
                response = f"Handle {handle} registered successfully"
        else:
            response = "Invalid register command. Usage: /register <handle>"
    
    elif command == '/store':
        print("wip")
    
    elif command == '/dir':
        print("wip")
    
    elif command == '/get':
        print("wip")
    
    else:
        response = "Unknown command"

    serverSocket.sendto(response.encode(), client_address)

def start_server():
    try:
        while True:
            message, client_address = serverSocket.recvfrom(2048)
            threading.Thread(target=handle_client_message, args=(message.decode(), client_address)).start()
    except KeyboardInterrupt:
        print("\nServer: Server shutting down")
    finally:
        serverSocket.close()

if __name__ == "__main__":
    start_server()

'''
try:
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        
        # Decode the message
        decoded_message = message.decode()
        print(f"Server: Received message: {decoded_message} from {clientAddress}")
        
        # Process the message (e.g., validate command, respond to client)
        response = f"Connection to the File Exchange Server is successful!"
        
        # Send response back to the client
        serverSocket.sendto(response.encode(), clientAddress)
        print(f"Server: Sent response to {clientAddress}")

except KeyboardInterrupt:
    print("\nServer: Server shutting down")

finally:
    # Close the socket when done
    serverSocket.close()
'''

