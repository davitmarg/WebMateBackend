from person import Person

user_sessions = dict()


def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = Person()
    return user_sessions[user_id]


def send_message(user_id, message):
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
    user_sessions[user_id] = Person()
    return True


