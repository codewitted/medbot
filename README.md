
# Robocop Medical Center Bot (Kodi)

A multi‐threaded client‐server application demonstrating basic **natural language processing** (NLP) and **dialogue management** for a medical center chatbot. Kodi assists users with symptom checks, appointment scheduling, FAQs, and more.

---

## 1. Overview

This project comprises:

- **`server.py`**: A multi‐threaded server that listens for connections and relays messages between:
  1. **User** client: A human chat interface.
  2. **Bot** client: Our intelligent chatbot “Kodi.”

- **`client_user.py`**: A simple terminal‐based interface for the human to type messages and receive Kodi’s replies.

- **`client_bot.py`**: The chatbot logic. It parses inputs via a dictionary of medical terms and runs a state machine for scheduling, FAQs, and fallback responses.


**Use Case**: Kodi is not meant to replace professional medical advice—rather, it shows how to parse limited user inputs, track dialogue context, and handle scheduling or FAQ queries in an academic setting.

---

## 2. Requirements

- **Python** >= 3.7 (tested with Python 3.8+).
- **No external libraries** (only Python’s standard library: `socket`, `threading`, `re`, etc.).

---

## 3. Installation & Setup

1. **Clone / Download** this repository.
2. **Ensure** you have Python 3.7 or higher installed.  
   - Check by running `python --version` or `python3 --version`.
3. **No further installation** steps needed (no `pip install` required unless you decide to add optional dependencies).

---

## 4. Running the Application

### 4.1 Manual Run

Open three separate terminals (or command prompts):

1. **Server**  
   ```
   python server.py
   ```
   - You should see a message like:  
     ```
     [SERVER] Listening on 127.0.0.1:5000
     ```

2. **Bot Client**  
   ```
   python client_bot.py
   ```
   - Prints something like:  
     ```
     [BOT] Connected to the server.
     ```

3. **User Client**  
   ```
   python client_user.py
   ```
   - Prints:  
     ```
     [USER] Connected to the server. Type your messages below.
     ```
   - Start typing your queries to Kodi, e.g. “Hello,” “I have a sore throat,” etc.

#### Expected Flow
1. **User** message → **Server** → **Bot**  
2. **Bot** processes input, sends reply → **Server** → **User**

## 5. Code Structure

```
.
├── server.py         # Multi-threaded socket server (Part B1)
├── client_user.py    # Human user client (Part B2)
├── client_bot.py     # Chatbot client (Part B3, Kodi's logic)
├── README.md         # This file
```

### 5.1 `server.py`
- **Handles** multiple concurrent connections via `threading`.
- Identifies clients by their first message: `"USER"` or `"BOT"`.
- **Relays** user messages to the bot, and bot messages to the user.

### 5.2 `client_user.py`
- **Prompts** the user in a loop:
  1. Read console input.
  2. Send to server → forwarded to bot.
  3. Receive the bot’s response from server, print on console.

### 5.3 `client_bot.py`
- **Parses** user input using a large dictionary (75+ medical domain words).
- Uses a **state machine** with states:
  - `GREETING`, `SYMPTOM_CHECK`, `TRIAGE_OPTIONS`, `SCHEDULING`, `FAQ`, and a final `GOODBYE`.
- Generates an **appropriate response** or fallback for unrecognized text.

### 5.4 `client_test.py` (Optional)
- **Automates** a list of user messages (like “Hello,” “I have a fever,” etc.) to test coverage of multiple conversation paths without manual typing.

### 5.5 `autotest.py` (Optional)
- **Starts** `server.py`, **starts** `client_bot.py`, then **runs** `client_test.py`.
- Finally, **terminates** the background processes for a single‐script automated test.

---

## 6. Troubleshooting

1. **Port Conflicts**  
   - If `127.0.0.1:5000` is taken, edit `PORT = 5000` in `server.py` to another free port, e.g. `PORT = 6000`.
2. **No Bot Response**  
   - Ensure you’ve started `client_bot.py` *before* the user tries to talk. Otherwise, the user’s messages have nowhere to go.
   - Check server logs to confirm it registered both “BOT” and “USER.”
3. **Connection Refused**  
   - Make sure the server is running first. Confirm network firewall isn’t blocking local sockets.

---

## 7. Disclaimer

> **This chatbot is for educational/demo purposes only.**  
> It does **not** provide actual medical advice. If you have health concerns, consult a qualified professional.


## 8. Contact

For any questions, issues, or suggestions, please reach out to:

- **Author**: Kev B
- **Email**: codewitted@gmail.com
- **GitHub**: [GitHub Profile](https://github.com/codewitted)

Feel free to open an issue or submit a pull request in the repository for any improvements or bug fixes.


**Thank you for using Kodi, the Robocop Medical Center Bot!** If you have questions or want to expand the domain (e.g., adding more advanced diagnosis logic), feel free to modify the state machine or dictionary to suit your needs.
```
