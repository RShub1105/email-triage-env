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
        "tasks": ["easy", "medium", "hard"],
        "actions": ["refund", "support", "ignore"]
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
    score = env.grade(action["action"])
    return {"score": score}

@app.get("/baseline")
def baseline():
    scores = []

    for task in ["easy", "medium", "hard"]:
        obs = env.reset(task)

        # simple rule-based agent
        if "refund" in obs["email_text"]:
            action = "refund"
        else:
            action = "support"

        score = env.grade(action)
        scores.append(score)

    return {
        "baseline_score": sum(scores) / len(scores),
        "task_scores": scores
    }

@app.get("/state")
def state():
    return env.state()