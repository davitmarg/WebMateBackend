import time
import os
from dotenv import load_dotenv
from openai import OpenAI

from service.ai.abstract_ai import AbstractAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=key
)


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


def shorten_string(s, max_length=400):
    if len(s) > max_length:
        return s[:max_length//2] + s[-max_length//2:]
    return s

def compute_similarity_fast(input_string, reference_string):
    input_string = shorten_string(input_string)
    reference_string = shorten_string(reference_string)

    return compute_similarity(input_string, reference_string)


class PersonGPT4oMini(AbstractAI):
    def __init__(self, name='(no name)', description='someone'):
        super().__init__()

    def get_system_prompt(self):
        return "Your name is WebMate AI and your job is to provide personalised suggestions based on the content of the page the user is viewing" + \
            "here is the description of the person who sends you the message:" + self.name + " : " + self.description + \
            ": Also carefully consider on which page the user currently is:" + \
            ": All of your responses should be very very short." + \
            "And you should try to suggest something related to the current page the user is vewing." + \
            "You should never inform the user about which page he is browsing, because it's obvious" + \
            "Concentrate on the content of the page and suggest something related" + \
            "Always concentrate on the details from webpages to provide more personalized responses" + \
            "And suggest your help about the questions and provide more information about the subjects if necessary." + \
            "Don't be formal, talk as if you are talking to a friend" + \
            "Keep your responses very very short, not more than 20 words unless the user asks for more"

    def reset_history(self):
        self.history = []
        self.update_description()
        self.last_page_suggestion_checked = False
        self.last_message_time = 0

    def send_message(self, message):
        if time.time() - self.last_message_time > 360:
            self.reset_history()

        self.last_message_time = time.time()
        self.history.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                *self.history[:-1],
                {"role": "user", "content": "I am currently on this page : " + self.last_page},
                self.history[-1]
            ],
            max_tokens=self.max_tokens
        )
        response = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": response})

        # keep only last k messages in the history
        k = 5
        if len(self.history) > k:
            self.history = self.history[-k:]

        return response

    def add_page(self, page):
        if page == self.last_page or len(page) == 0:
            return

        if compute_similarity_fast(self.last_page, page) > 0.6:
            return

        self.last_page_suggestion_checked = False
        self.last_page = page
        self.page_history.append(page)
        if len(self.page_history) > 6:
            self.update_description()

    def update_description(self):
        system_prompt = f"""
      I will provide the latest pages that {self.name} has browsed,
      and you adjust this description of {self.name} if necessary.
      Also, here is previous description of the guy '{self.description}'
      Additionally, note that it's just some pages that {self.name} has browsed
      and they don't have to reflect his actual interests,
      so don't concentrate on them too much.
      Write a very very short paragraph and keep only the necessary information.
    """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{self.page_history}"}
            ],
            max_tokens=self.max_tokens * 3
        )

        response = response.choices[0].message.content
        self.description = response
        self.page_history = []
        return response

    def should_suggest(self):
        if self.last_page_suggestion_checked:
            return False

        self.last_page_suggestion_checked = True

        prompt = """
    Given the page info the user is currently browsing,
    tell whether the user needs help/suggestion about the page or not.
    Return only true or false without extra text.
    """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": self.last_page}
            ],
            max_tokens=3
        )

        response = response.choices[0].message.content
        response_bool = False

        if 'false' in response:
            response_bool = False
        elif 'true' in response:
            response_bool = True
        else:
            response_bool = False

        return response_bool

    def get_suggestion(self):
        prompt = """
    Given the page info the user is currently browsing,
    suggest a very very short message to the user or offer help if you know how to help
    and by specific about the suggestion, don't suggest something very general
    Use english if most of the text is in english and don't be formal, talk as if you are talking to a friend
    """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": self.last_page}
            ],
            max_tokens=self.max_tokens
        )
        response = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": response})
        return response
