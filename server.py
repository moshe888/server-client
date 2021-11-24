import os
import socket
import threading

HOST = '127.0.0.1' 
PORT = 8888
ADDR = (HOST, PORT)
SIZE = 2048
FORMAT = "utf-8"
SERVER_DATA= "server_data"

def handle_client(conn, addr):
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
  
        if cmd == "LIST":
            files = os.listdir(SERVER_DATA)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA, name)
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))


        elif cmd == "DOWNLOAD":
            filename = data[1]
            if filename not in os.listdir(SERVER_DATA):
                send_data = "OK@The file does not exist"
            else:
                with open(f"{SERVER_DATA}/{filename}", "r") as f:
                    send_data = "FILE@ " + f.read()
                    
            conn.send(send_data.encode(FORMAT))   
        elif cmd == "CHAT":
            while True:
                message = input(str("Me : "))
              
                conn.send(message.encode())
                message = conn.recv(1024)
                message = message.decode()
                print(cmd, ":", message)
       

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}.")

    conn, addr = server.accept()
    handle_client(conn, addr)
    

if __name__ == "__main__":
    main()