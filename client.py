import socket
import threading

username = input("Pick a username: ")
serverAddress = '127.0.0.1'
serverPort = 4760
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverAddress, serverPort))

#CLIENT RECEIVES A MESSAGE
def receive():
    while True:
        try:
            message = clientSocket.recv(1024).decode("utf-8")
            if message == "What is you Username?: ":
                clientSocket.send(username.encode("utf-8"))
                clientSocket.send(f"New User {username} has entered the chat!".encode("utf-8"))
                print(f"Welcome to the chat {username}!\n")
                print("Type /quit to leave the chat room.\n")
            else:
                print(message)
        except Exception as e:
            print(f"ClientReceive Error: {e}\n")
            clientSocket.close()
            break

#CLIENT SENDS A MESSAGE   
def send():
    while True:
        message = f"{username}: {input()}"
        clientSocket.send(message.encode("utf-8"))

#MY LOVELY SEND AND RECEIVE THREADS 
receiveThread = threading.Thread(target=receive)
receiveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()
