import socket
import threading

HOST = '127.0.0.1'  # or 'localhost'
PORT = 5000

# Global references to sockets
client_sockets = {}
client_lock = threading.Lock()

def handle_client(conn, addr):
    """
    Each connected client runs in its own thread.
    We identify the client as either 'USER' or 'BOT' 
    based on the first message they send.
    Then we forward messages accordingly.
    """
    print(f"[SERVER] New connection from {addr}")

    try:
        # First message determines role
        initial_msg = conn.recv(1024).decode('utf-8').strip()
        if initial_msg == "USER":
            client_type = "USER"
        elif initial_msg == "BOT":
            client_type = "BOT"
        else:
            # Default fallback if unknown, treat as USER
            client_type = "USER"

        with client_lock:
            client_sockets[client_type] = conn
        print(f"[SERVER] {client_type} registered from {addr}")

        # Now listen for incoming messages and forward them
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Client disconnected

            message = data.decode('utf-8')
            # Forward the message to the other client (if available)
            other_type = "BOT" if client_type == "USER" else "USER"

            with client_lock:
                if other_type in client_sockets:
                    client_sockets[other_type].sendall(message.encode('utf-8'))
                else:
                    # No other client connected yet
                    conn.sendall("No partner connected yet.".encode('utf-8'))

    except Exception as e:
        print(f"[SERVER] Exception with {addr}: {e}")
    finally:
        # Cleanup
        with client_lock:
            if client_type in client_sockets:
                del client_sockets[client_type]
        conn.close()
        print(f"[SERVER] Connection closed with {addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
