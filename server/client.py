import random
from .models import EmailAction, EmailObservation

class EmailEnv:

    def __init__(self):
        self.tasks = {
    "easy": [
        ("I want a refund for my order #1234", "refund"),
        ("Please return my money", "refund"),
        ("I need a refund for a wrong item", "refund"),

        ("Can you help me reset my password?", "support"),
        ("I cannot login to my account", "support"),
        ("Need help accessing my account", "support"),
    ],

    "medium": [
        ("I want a refund but also need help logging in", "refund"),
        ("My product arrived damaged and I need assistance", "support"),
        ("I was charged twice, please help", "refund"),
        ("I need support and maybe a refund", "support"),
    ],

    "hard": [
        ("I've been charged twice but also can't login anymore", "refund"),
        ("This service is terrible, I want to cancel everything", "refund"),
        ("I'm not sure what's wrong but nothing works properly", "support"),
    ]
}

        self.current_email = None
        self.correct_action = None
        self.current_task = "easy"

    def reset(self, task="easy"):
        self.current_task = task
        self.current_email, self.correct_action = random.choice(self.tasks[task])

        return {"email_text": self.current_email}

    def step(self, action):

        predicted = action["action"]

        if predicted == self.correct_action:
            reward = 1.0

        elif predicted in ["refund", "support"]:
            reward = 0.3

        else:
            reward = -0.5

        done = True

        return {"email_text": self.current_email}, reward, done, {}

    # ✅ GRADER
    def grader(self, action):
        correct = self.correct_action

        if action == correct:
            return 1.0

        # partial credit
        if correct == "refund" and action == "support":
            return 0.5

        if correct == "support" and action == "ignore":
            return 0.2

        return 0.0

    def state(self):
        return {
            "email": self.current_email,
            "task": self.current_task
        }
   
    def smart_classify(self, email):
        email = email.lower()

        if "refund" in email or "money back" in email or "return" in email:
            return "refund"

        if "help" in email or "issue" in email or "problem" in email:
            return "support"

        if "angry" in email or "frustrating" in email:
            return "support"

        return "ignore"