import socket
import sys

HOST = "127.0.0.1"
PORT = 8888
FORMAT = "utf-8"
SIZE = 2048

def main():
    global HOST
    
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
        
    ADDR = (HOST, PORT)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    receive = True

    while True:
        if receive: 
            data = client.recv(SIZE).decode(FORMAT)  
            cmd, msg= data.split("@")
             
            if cmd == "OK":
                print(f"{msg}")
            elif cmd == "FILE":
                with open(f"downloaded_{filename}", "w") as f:
                    f.write(msg)
                
                
        receive = True
 
        data = input("> ")
        data = data.split(" ")
        cmd = data[0]
       
        if cmd == "CHAT":
            name = data[1]
            client.send(cmd.encode(FORMAT))
            while True:
                message = client.recv(1024)
                message = message.decode()
                print(name, ":", message)
                message = input(str("Me : "))
              
                client.send(message.encode())
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))  
        elif cmd == "UPLOAD":
            path = data[1]

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
        
        elif cmd == "DOWNLOAD":
            filename = data[1]
            send_data = f"{cmd}@{filename}"
            client.send(send_data.encode(FORMAT))
        else:
            print("Invalid command")
            receive = False
            
        

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()
