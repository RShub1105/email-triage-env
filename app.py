import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from client import EmailEnv

app = FastAPI()



@app.get("/")
def home():
    return {"message": "Email Env Running 🚀"}

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "name": "easy",
                "description": "Clear intent emails (explicit refund or support requests)"
            },
            {
                "name": "medium",
                "description": "Emails with multiple intents (refund + support mixed)"
            },
            {
                "name": "hard",
                "description": "Ambiguous or emotional emails where intent is unclear"
            }
        ],
        "action_schema": {
            "type": "string",
            "enum": ["refund", "support", "ignore"]
        }
    }

# RESET
@app.post("/reset")
def reset(task: str = "easy"):
    env = EmailEnv()
    obs = env.reset(task)
    return {"observation": obs}




# STEP
@app.post("/step")
def step(action: dict):
    env = EmailEnv()

    try:
        result = env.step("ignore")
        if isinstance(result, tuple) and len(result) == 4:
            obs, reward, done, info = result
        else:
            obs, reward, done, info = result, 0, False, {}
    except Exception as e:
        return {"error": str(e)}

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.post("/grader")
def grader(action: dict):
    env = EmailEnv()
    try:
        score = env.grader(action["action"])
    except Exception:
        score = 0.0
    return {"score": float(score)}


@app.get("/baseline")
def get_baseline():
    scores = []
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        try:
            env = EmailEnv()  # fresh env each time

            obs = env.reset(task)

            action = {"action": "ignore"}

            result = env.step(action)

            if isinstance(result, tuple) and len(result) >= 2:
                reward = float(result[1])
            else:
                reward = 0.0

            scores.append(reward)

        except Exception as e:
            print(f"Baseline error on {task}:", e)
            scores.append(0.0)

    return {
        "baseline_score": sum(scores) / len(scores) if scores else 0.0,
        "task_scores": scores
    }


@app.get("/state")
def state():
    env = EmailEnv()
    try:
        return env.state()
    except:
        return {"state": "unknown"}


@app.get("/health")
def health():
    return {"status": "ok"}