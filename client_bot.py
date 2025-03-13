import socket
import re

HOST = '127.0.0.1'
PORT = 5000

# ---------------------------------------------------------
# 1. Large Dictionary (25 original + ~50 new) = 75+ entries
# ---------------------------------------------------------
BOT_DICTIONARY = {
    "hello":     {"type": "greeting"},
    "hi":        {"type": "greeting"},
    "hey":       {"type": "greeting"},
    "help":      {"type": "request"},
    "yes":       {"type": "affirmation"},
    "no":        {"type": "negation"},
    "sore":      {"type": "symptom"},
    "throat":    {"type": "symptom"},
    "fever":     {"type": "symptom"},
    "cough":     {"type": "symptom"},
    "dizzy":     {"type": "symptom"},
    "appointment": {"type": "noun"},
    "schedule":  {"type": "verb"},
    "tomorrow":  {"type": "time"},
    "day":       {"type": "time"},
    "next":      {"type": "time"},
    "week":      {"type": "time"},
    "doctor":    {"type": "role"},
    "general":   {"type": "adjective"},
    "practitioner": {"type": "role"},
    "insurance": {"type": "noun"},
    "hours":     {"type": "noun"},
    "monday":    {"type": "time"},
    "tuesday":   {"type": "time"},
    "wednesday": {"type": "time"},
    "thursday":  {"type": "time"},
    "friday":    {"type": "time"},
    "saturday":  {"type": "time"},
    "sunday":    {"type": "time"},
    "morning":   {"type": "time"},
    "afternoon": {"type": "time"},
    "evening":   {"type": "time"},
    "thank":     {"type": "gratitude"},
    "thanks":    {"type": "gratitude"},
    "bye":       {"type": "farewell"},
    "goodbye":   {"type": "farewell"},
    "robocop":   {"type": "brand"},
    "medical":   {"type": "adjective"},
    "center":    {"type": "noun"},
    "feeling":   {"type": "verb"},
    "better":    {"type": "adjective"},
    "open":      {"type": "verb"},
    "night":     {"type": "time"},
    "pain":      {"type": "symptom"},
    "headache":  {"type": "symptom"},
    "backache":  {"type": "symptom"},
    "infection": {"type": "symptom"},
    "cold":      {"type": "symptom"},
    "chills":    {"type": "symptom"},
    "scheduling": {"type": "noun"},
    "clinic":    {"type": "noun"},
    "pharmacy":  {"type": "noun"},
    "refill":    {"type": "noun"},
    "reminder":  {"type": "noun"},
    "prescription": {"type": "noun"},
    "blood":     {"type": "noun"},
    "pressure":  {"type": "noun"},
    "diabetes":  {"type": "noun"},
    "heart":     {"type": "noun"},
    "specialist": {"type": "role"},
    "checkup":   {"type": "noun"},
    "test":      {"type": "noun"},
    "results":   {"type": "noun"},
    "open":      {"type": "verb"},
    "closed":    {"type": "adjective"},
    "cardiology":{"type": "noun"},
    "dermatology":{"type": "noun"},
    "optometry": {"type": "noun"},
    "zero":      {"type": "number"},
    "one":       {"type": "number"},
    "two":       {"type": "number"},
    "three":     {"type": "number"},
    "four":      {"type": "number"},
    "five":      {"type": "number"},
    "six":       {"type": "number"},
    "seven":     {"type": "number"},
    "eight":     {"type": "number"},
    "nine":      {"type": "number"},
    "ten":       {"type": "number"},
    "2":         {"type": "number"},
    "3":         {"type": "number"},
    "4":         {"type": "number"},
    "pm":        {"type": "time"},
}

# ---------------------------------------------------------
# 2. Simple State Machine
# ---------------------------------------------------------
ST_GREETING       = 0
ST_SYMPTOM_CHECK  = 1
ST_TRIAGE_OPTIONS = 2
ST_SCHEDULING     = 3
ST_FAQ            = 4
ST_GOODBYE        = 5

# Context dictionary to track the current state, appointment times, etc.
context = {
    "state": ST_GREETING,
    "appointment_time": None,
    "user_symptom": None
}

def parse_input(user_input):
    """
    Tokenizer + parser: splits user input on non-alphanumerics,
    then checks each token in BOT_DICTIONARY.
    """
    tokens = re.split(r'[^a-zA-Z0-9]+', user_input.lower())
    recognized = set()
    for tk in tokens:
        if tk in BOT_DICTIONARY:
            recognized.add(tk)
    return recognized

def handle_faq(recognized):
    """
    Handles typical FAQ questions or transitions back to scheduling if user requests it.
    """
    global context

    # If user wants to schedule an appointment while in FAQ:
    if {"appointment", "schedule"}.intersection(recognized):
        context["state"] = ST_SCHEDULING
        return ("Let’s schedule an appointment. "
                "When are you available (e.g., 'tomorrow at 2 PM')?")

    # Check for clinic hours
    elif "hours" in recognized:
        return "We are open Monday to Friday, 8 AM to 5 PM. Anything else?"

    # Check for insurance
    elif "insurance" in recognized:
        return "We accept most major insurance providers. Any other questions?"

    # Check for farewell
    elif {"bye", "goodbye"}.intersection(recognized):
        context["state"] = ST_GOODBYE
        return (
            "Thank you for choosing Robocop Medical Center. "
            "Take care, and I hope you feel better soon. GOODBYE"
        )

    # Check for gratitude
    elif {"thank", "thanks"}.intersection(recognized):
        return "You’re welcome! Anything else I can help you with?"

    # Fallback
    return (
        "You can ask about clinic hours, insurance, or say 'schedule' "
        "if you want to book an appointment. What would you like to do?"
    )

def generate_bot_response(user_input):
    """
    Main logic for Kodi's conversation flow,
    using the global 'context' to track states and recognized tokens.
    """
    global context
    recognized = parse_input(user_input)
    state = context["state"]

    # ----------------
    # 1. GREETING
    # ----------------
    if state == ST_GREETING:
        # If user greets, or basically says anything non-empty, we proceed
        if recognized or user_input.strip():
            context["state"] = ST_SYMPTOM_CHECK
            return ("Hello! I’m Kodi, your Robocop Medical Center assistant. "
                    "How can I help you? Could you describe your main symptom?")
        else:
            return "Hello! Please say hi or hello so we can begin."

    # ----------------
    # 2. SYMPTOM_CHECK
    # ----------------
    elif state == ST_SYMPTOM_CHECK:
        possible_symptoms = {
            "sore", "throat", "fever", "cough", "dizzy", "pain",
            "headache", "backache", "infection", "cold", "chills"
        }
        found_symptoms = possible_symptoms.intersection(recognized)

        if found_symptoms:
            # Store a single symptom
            context["user_symptom"] = found_symptoms.pop()
            context["state"] = ST_TRIAGE_OPTIONS
            return (f"Sorry to hear you have {context['user_symptom']}. "
                    "Would you like me to schedule an appointment or offer basic advice?")
        else:
            # Possibly user wants hours/insurance directly
            if "hours" in recognized or "insurance" in recognized:
                context["state"] = ST_FAQ
                return handle_faq(recognized)
            else:
                return "I'm not sure I understand your symptom. Could you describe it more clearly?"

    # ----------------
    # 3. TRIAGE_OPTIONS
    # ----------------
    elif state == ST_TRIAGE_OPTIONS:
        if {"appointment", "schedule"}.intersection(recognized):
            context["state"] = ST_SCHEDULING
            return ("Let’s schedule an appointment. "
                    "When are you available (e.g., 'tomorrow at 2 PM')?")
        elif "advice" in user_input.lower():
            context["state"] = ST_FAQ
            return ("For minor symptoms, rest and hydration can help. "
                    "If you have severe issues, we recommend seeing a doctor. "
                    "Anything else you'd like to know?")
        else:
            # Possibly user just said yes/no
            if "yes" in recognized:
                context["state"] = ST_SCHEDULING
                return "Great! When are you available for an appointment?"
            elif "no" in recognized:
                context["state"] = ST_FAQ
                return ("No worries. Is there anything else you'd like? "
                        "You could ask about hours or insurance, or schedule later.")
            else:
                return "I’m not sure what you mean. Would you like an appointment or just advice?"

    # ----------------
    # 4. SCHEDULING
    # ----------------
    elif state == ST_SCHEDULING:
        time_keywords = {
            "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday", "afternoon", "morning", "evening",
            "2", "3", "4", "pm", "am", "next"
        }
        if time_keywords.intersection(recognized):
            context["appointment_time"] = user_input
            context["state"] = ST_FAQ
            return (f"Your appointment is set for '{user_input}'. "
                    "Anything else I can help you with? (Type 'hours' or 'insurance' or 'schedule')")
        else:
            return "Please specify a day or time (e.g., 'tomorrow at 2 PM')."

    # ---------------
    # 5. FAQ
    # ---------------
    elif state == ST_FAQ:
        return handle_faq(recognized)

    # ---------------
    # 6. GOODBYE
    # ---------------
    elif state == ST_GOODBYE:
        return "GOODBYE"

    # ---------------
    # Fallback
    # ---------------
    return "I’m not sure how to handle that. Could you rephrase?"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Identify as BOT
        s.sendall("BOT".encode('utf-8'))
        print("[BOT] Connected to the server.")

        while True:
            data = s.recv(1024)
            if not data:
                print("[BOT] Server closed the connection.")
                break

            user_msg = data.decode('utf-8').strip()
            if not user_msg:
                continue

            bot_reply = generate_bot_response(user_msg)
            s.sendall(bot_reply.encode('utf-8'))

            # If the bot says "GOODBYE," terminate
            if "GOODBYE" in bot_reply.upper():
                print("[BOT] Conversation ended. Shutting down.")
                break

if __name__ == "__main__":
    main()
