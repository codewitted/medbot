import socket

HOST = '127.0.0.1'
PORT = 5000

def main():
    # Connect to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Identify as USER
        s.sendall("USER".encode('utf-8'))

        print("[USER] Connected to the server. Type your messages below.")

        # Start a simple loop: 
        #  - read user input from console
        #  - send to server
        #  - receive potential bot responses from server in a non-blocking manner if possible
        # For simplicity, we do a blocking approach: type something, wait for the response.
        while True:
            user_input = input("You: ")
            if not user_input:
                user_input = " "  # avoid empty string issues

            s.sendall(user_input.encode('utf-8'))

            # Try to receive from server (which is actually from the BOT)
            response = s.recv(1024)
            if not response:
                print("[USER] Server closed the connection.")
                break

            bot_message = response.decode('utf-8')
            print(f"Kodi: {bot_message}")

            if "GOODBYE" in bot_message.upper():
                print("[USER] Ending conversation as bot said goodbye.")
                break

if __name__ == "__main__":
    main()
