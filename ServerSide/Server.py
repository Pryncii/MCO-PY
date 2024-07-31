from socket import *
import threading
import os

# Define server port and create UDP socket
serverPort = 12345
serverIP = '127.0.0.1'
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('Server: The server is ready to receive')

clients = {}
messages = {}
file_transfers = {}  # To track ongoing file transfers


def handle_client_message(message, client_address):
    global clients, file_transfers

    command_parts = message.strip().split()
    command = command_parts[0]
    IP = command_parts[1]
    port = int(command_parts[2])

    if command == '/join':
        if port == serverPort and IP == serverIP:
            response = f"Welcome! Your address is {client_address}"
        else:
            response = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            
        serverSocket.sendto(response.encode(), client_address)

    elif command == '/msg':
        parts = message.strip().split(' ', 2)
        print(parts)
        print(clients)
        handle = parts[1]
        msg = parts[2]
        sender = clients[client_address]
        response1 = f"Message '{msg}' sent to {handle}"
         # Find the address of the recipient
        recipient_address = None
        for addr, name in clients.items():
            if name == handle:
                recipient_address = addr
                break

        if recipient_address:
            response = f"{sender}: {msg}"
            messages[recipient_address].append(response)
        
        serverSocket.sendto(response1.encode(), client_address)

    elif command == '/viewmsg':
        
        # Join all messages into a single string for the client
        response = "\n".join(messages[client_address])
        serverSocket.sendto(response.encode(), client_address)

    elif command == '/broadcast':
        parts = message.strip().split(' ', 1)
        print(parts)
        print(clients)
        msg = parts[1]
        sender = clients[client_address]
        response1 = f"Message '{msg}' broadcasted"
         # Find the address of the recipient
        for addr, name in clients.items():
            if addr != client_address:
                response = f"{sender}(broadcast): {msg}"
                messages[addr].append(response)
        
        serverSocket.sendto(response1.encode(), client_address)

    
    elif command == '/leave':
        if client_address in clients:
            response = f"{clients[client_address]}: Disconnected from the server."
            del clients[client_address]
        serverSocket.sendto(response.encode(), client_address)
    
    elif command == '/register':
        if len(command_parts) == 2:
            handle = command_parts[1]

            if handle in clients.values():
                response = f"Error: Handle '{handle}' is already in use."
            
            else:
                clients[client_address] = handle
                messages[client_address] = []
                messages[client_address].append("Message Log: \n")
                response = f"Handle {handle} registered successfully"
        else:
            response = "Invalid register command. Usage: /register <handle>"

        serverSocket.sendto(response.encode(), client_address)
    
    elif command == '/store':
        if len(command_parts) == 2:
            filename = command_parts[1]
            response = f"Ready to receive file: {filename}"
            serverSocket.sendto(response.encode(), client_address)
            file_transfers[client_address] = {'filename': filename, 'file_data': b''}

        else:
            response = "Invalid store command. Usage: /store <filename>"
            serverSocket.sendto(response.encode(), client_address)
    
    elif command == '/dir':
        files = os.listdir("./Server Files")
        if not files:
            response = "No files found in the server."
        else:
            response = "Files in server:\n" + "\n".join(files)
        serverSocket.sendto(response.encode(), client_address)
    
    elif command == '/get':
        if len(command_parts) == 2:
            filename = command_parts[1]
            file_path = f"./Server Files/{filename}"

            if os.path.exists(file_path):
                response = f"Ready to send file: {filename}"
                serverSocket.sendto(response.encode(), client_address)

                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(1024)
                        if chunk:
                            serverSocket.sendto(chunk, client_address)
                        else:
                            break
                    serverSocket.sendto(b'EOF', client_address)
                response = f"{clients[client_address]}: File {filename} sent successfully."
            else:
                response = f"Error: File {filename} not found."
        else:
            response = "Invalid get command. Usage: /get <filename>"

        serverSocket.sendto(response.encode(), client_address)
    
    else:
        response = "Unknown command"
        serverSocket.sendto(response.encode(), client_address)


def handle_file_transfer(chunk, client_address):
    global file_transfers

    if client_address in file_transfers:
        # print(f"Server chunk {chunk}")
        if chunk == b'EOF':
            filename = file_transfers[client_address]['filename']
            file_data = file_transfers[client_address]['file_data']
            file_path = f"./Server Files/{filename}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            response = f"{clients[client_address]}: File {filename} stored successfully."
            serverSocket.sendto(response.encode(), client_address)
            del file_transfers[client_address]
        else:
            file_transfers[client_address]['file_data'] += chunk
            response = None  # No response needed for file chunks
    else:
        response = "Error: No ongoing file transfer for this client."
        serverSocket.sendto(response.encode(), client_address)

def start_server():
    try:
        while True:
            chunk, client_address = serverSocket.recvfrom(2048)
            if client_address in file_transfers and chunk[:5] != b'/join' and chunk[:6] != b'/leave' and chunk[:9] != b'/register' and chunk[:6] != b'/store' and chunk[:4] != b'/dir' and chunk[:4] != b'/get':
                handle_file_transfer(chunk, client_address)
            else:
                threading.Thread(target=handle_client_message, args=(chunk.decode(), client_address)).start()
    except KeyboardInterrupt:
        print("\nServer: Server shutting down")
    finally:
        serverSocket.close()

if __name__ == "__main__":
    start_server()

