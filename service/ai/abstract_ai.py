class AbstractAI:
    def __init__(self, name='(no name)', description='someone'):
        self.name = name
        self.description = description
        self.history = []
        self.last_page = ""
        self.page_history = []
        self.last_page_suggestion_checked = False
        self.max_tokens = 50
        self.last_message_time = 0

    def get_system_prompt(self):
        return "some system prompt"

    def reset_history(self):
        pass

    def send_message(self, message):
        pass

    def add_page(self, page):
        pass

    def update_description(self):
        pass

    def get_suggestion(self):
        pass
