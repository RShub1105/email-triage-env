from fastapi import FastAPI
from email_env.client import EmailEnv

app = FastAPI()

env = EmailEnv()


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
    obs = env.reset(task)
    return {"observation": obs}




# STEP
@app.post("/step")
def step(action: dict):
    if hasattr(env, 'step') and callable(getattr(env, 'step')):
        result = env.step(action)
        if isinstance(result, tuple) and len(result) == 4:
            obs, reward, done, info = result
        else:
            obs, reward, done, info = result, 0, False, {}
    else:
        obs, reward, done, info = {}, 0, False, {"error": "step method not available"}
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.post("/grader")
def grader(action: dict):
    score = env.grader(action["action"])
    return {"score": score}

@app.get("/baseline")
def baseline():
    scores = []

    for task in ["easy", "medium", "hard"]:
        obs = env.reset(task)

        email = obs["email_text"]

        # simple rule-based agent
        if "refund" in email.lower():
            action = "refund"
        elif "help" in email.lower() or "issue" in email.lower():
            action = "support"
        else:
            action = "support"

        obs, reward, done, info = env.step({"action": action})

        score = env.grader(action)

        scores.append(score)

    return {
        "baseline_score": sum(scores) / len(scores),
        "task_scores": scores
    }

@app.get("/state")
def state():
    return env.state()

@app.get("/health")
def health():
    return {"status": "ok"}