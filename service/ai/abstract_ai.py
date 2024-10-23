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
        self.client = None

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

def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    if m < n:
        s, t = t, s
        m, n = n, m
    d = [list(range(n + 1))] + [[i] + [0] * n for i in range(1, m + 1)]
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    return d[m][n]


def compute_similarity(input_string, reference_string):
    distance = levenshtein_distance(input_string, reference_string)
    max_length = max(len(input_string), len(reference_string))
    similarity = 1 - (distance / max_length)
    return similarity


def shorten_string(s, max_length=3000, sampling_steps=200):
    if len(s) <= max_length:
        return s
    length = len(s)
    sample_length = max_length // sampling_steps

    shortened_string = ""

    for i in range(0, length, length // sampling_steps):
        shortened_string += s[i:i + sample_length]

    return shortened_string


def compute_similarity_fast(input_string, reference_string):
    return compute_similarity(shorten_string(input_string), shorten_string(reference_string))