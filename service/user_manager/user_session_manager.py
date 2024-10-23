from service.ai.nemotron_70b_hf import Nemotoron70bHF
from service.ai.persongpt4omini import PersonGPT4oMini

user_sessions = dict()

MODEL_NAME = "Nemotoron70bHF"

def get_session(user_id):
    if user_id not in user_sessions:
        if MODEL_NAME == "PersonGPT4oMini":
            user_sessions[user_id] = PersonGPT4oMini()
        elif MODEL_NAME == "Nemotoron70bHF":
            user_sessions[user_id] = Nemotoron70bHF()
    return user_sessions[user_id]


def send_message(user_id, message):
    print(f"message '{message}' from {user_id}")
    session = get_session(user_id)
    return session.send_message(message)


def should_suggest(user_id):
    session = get_session(user_id)
    return session.should_suggest()


def get_suggestion(user_id):
    session = get_session(user_id)
    return session.get_suggestion()


def add_page(user_id, page):
    session = get_session(user_id)
    session.add_page(page)
    return True


def update_description(user_id):
    session = get_session(user_id)
    return session.update_description()


def reset(user_id):
    user_sessions[user_id] = PersonGPT4oMini()
    return True


