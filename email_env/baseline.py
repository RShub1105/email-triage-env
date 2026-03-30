import requests
import os
import random

random.seed(42)


BASE_URL = "https://rshuge-email-triage-env.hf.space"  

def smart_agent(email):
    email = email.lower()

    if "refund" in email or "money back" in email or "return" in email:
        return "refund"

    if "help" in email or "issue" in email or "problem" in email:
        return "support"

    if "frustrating" in email or "angry" in email:
        return "support"

    return "ignore"


def run_task(task):
    # reset
    res = requests.post(f"{BASE_URL}/reset", params={"task": task})
    email = res.json()["observation"]["email_text"]

    # agent decides
    action = smart_agent(email)

    # step
    step_res = requests.post(f"{BASE_URL}/step", json={"action": action})
    reward = step_res.json()["reward"]

    # grader
    grade_res = requests.post(f"{BASE_URL}/grader", json={"action": action})
    score = grade_res.json()["score"]

    return reward, score


def main():
    tasks = ["easy", "medium", "hard"]
    scores = []

    for task in tasks:
        reward, score = run_task(task)
        print(f"{task.upper()} → reward: {reward}, score: {score}")
        scores.append(score)

    print("\nFINAL SCORE:", sum(scores) / len(scores))


if __name__ == "__main__":
    main()