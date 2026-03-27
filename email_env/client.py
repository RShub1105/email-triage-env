import random

class EmailEnv:

    def __init__(self):
        self.tasks = {
            "easy": [
                ("I want a refund", "refund"),
                ("Help me with my account", "support"),
            ],
            "medium": [
                ("I need refund but also help", "refund"),
                ("My order is broken, what to do?", "support"),
            ],
            "hard": [
                ("This is frustrating, fix this now!", "support"),
                ("I am unhappy with the service", "support"),
            ]
        }

        self.current_email = None
        self.correct_action = None
        self.current_task = "easy"

    def reset(self, task="easy"):
        self.current_task = task
        self.current_email, self.correct_action = random.choice(self.tasks[task])

        return {"email_text": self.current_email}

    # ✅ THIS WAS MISSING OR BROKEN
    def step(self, action):

        predicted = action["action"]

        if predicted == self.correct_action:
            reward = 1.0
        elif predicted in ["refund", "support"]:
            reward = 0.5
        else:
            reward = -1.0

        done = True

        return {"email_text": self.current_email}, reward, done, {}

    # ✅ GRADER
    def grade(self, predicted):
        if predicted == self.correct_action:
            return 1.0
        elif predicted in ["refund", "support"]:
            return 0.5
        else:
            return 0.0

    def state(self):
        return {
            "email": self.current_email,
            "task": self.current_task
        }