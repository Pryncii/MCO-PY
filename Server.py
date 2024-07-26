from socket import *

# Define server port and create UDP socket
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')

try:
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        
        # Decode the message
        decoded_message = message.decode()
        print(f"Received message: {decoded_message} from {clientAddress}")
        
        # Process the message (e.g., validate command, respond to client)
        response = f"Message '{decoded_message}' received"
        
        # Send response back to the client
        serverSocket.sendto(response.encode(), clientAddress)
        print(f"Sent response to {clientAddress}")

except KeyboardInterrupt:
    print("\nServer shutting down")

finally:
    # Close the socket when done
    serverSocket.close()
