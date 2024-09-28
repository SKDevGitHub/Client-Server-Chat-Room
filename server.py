import socket
import threading

#CLIENTS LIST AND THEIR ASSOCIATED USERNAMES
clients = []
usernames = []

#REMOVES THE CLIENT FROM THE SERVER
def clientRemover(client):
    if client in clients:
        place = clients.index(client)
        username = usernames[place]
        messageToAll(f"{username} has left the chat".encode("utf-8"))
        print(f"{username} has left the chat")
        clients.remove(client)
        usernames.remove(username)
        print(f"Number of Users: {len(usernames)}")
        print(f"Current Users: {usernames}\n")
        client.close()

#HANDLES ALL MESSAGES AND DEALS WITH EACH MESSAGE ACCOURDINGLY (PRIVATE, QUIT, NORMAL)
def messageHandle(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            
            if ':' in message:
                splitter = message.split(':')
                
                #CHECK FOR QUIT TO QUIT CLIENT
                if splitter[1] == " /quit":
                    clientRemover(client)
                    break
                
                if len(splitter) > 1:
                    check = splitter[1]
                else:
                    check = splitter[0]
                    
                if check.startswith(' @'):
                    target, pMessage = decoder(message)
                    privateMessage(client, target, pMessage)
                else:
                    print(f"Universal Message from {message}")
                    messageToAll(message.encode("utf-8"), sender=client)
        except Exception as e:
            print(f"MessageHandle Error: {e}\n")
            clientRemover(client)
            break
    
#SENDS MESSAGE TO ALL CLIENTS
def messageToAll(message, sender = None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except Exception as e:
                print(f"MessageToAll Error: {e}\n")
                clientRemover(client)
                break

#DETERMINES WHAT THE RECEIVER OF THE PRIVATE MESSAGE IS AS WELL AS THE MESSAGE ITSELF
def decoder(message2):
    try:
        message = message2.split(": ")
        message1 = message[1].split('@')
        target = message1[1]
        pMessage = message[2]
        receiver = target
        return receiver, pMessage
    except Exception as e:
        print(f"Decoder Error: {e}\n")
        return None, None

#SENDS THE PRIVATE MESSAGE TO ONLY THE TARGET RECEIVER                
def privateMessage(sender, target, message):
    check = clients.index(sender)
    senderprint = usernames[check]
    if target in usernames:
        targetPlace = usernames.index(target)
        targetClient = clients[targetPlace]
        try:
            targetClient.send(f"Private Message from {senderprint}: {message}".encode("utf-8"))
            print(f"Private Message from {senderprint} to {target}: {message}")
        except Exception as e:
            print(f"PrivateMessage Error: {e}\n")
            clientRemover(targetClient)
    else:
        sender.send(f"User {target} not found.".encode("utf-8"))

#SERVER STARTUP
def startServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', 4760))
    serverSocket.listen(5)
    print("Server Started. Waiting for Client Connections...\n")
    
    while True:
        clientSocket, clientAddress = serverSocket.accept()
        print(f"\nConnection from {clientAddress} established.")
        
        clientSocket.send("What is you Username?: ".encode("utf-8"))
        username = clientSocket.recv(1024).decode("utf-8")
        usernames.append(username)
        clients.append(clientSocket)
        
        print(f"Username of the new client is {username}")
        print(f"Number of Users: {len(usernames)}")
        print(f"Current Users: {usernames}")
        
        clientThread = threading.Thread(target=messageHandle, args = (clientSocket,))
        clientThread.start()
        print("Client Thread Started\n")

#ON SCRIPT RUN
if __name__ == "__main__":
    startServer()
