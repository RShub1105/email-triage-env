import os
from fastapi import FastAPI, HTTPException
from .client import EmailEnv
from .models import EmailAction

app = FastAPI()
# Global instance for the hackathon (simplest way to maintain state for single-agent eval)
env_instance = EmailEnv()

@app.get("/")
def home():
    return {"message": "Email Env Running 🚀"}

@app.post("/reset")
def reset(task: str = "easy"):
    obs = env_instance.reset(task)
    return {"observation": obs}

@app.post("/step")
def step(action: dict):
    # Standardize input: handle {"action": "val"} or just "val"
    act_val = action.get("action", action)
    if isinstance(act_val, dict):
        act_val = act_val.get("action")
        
    try:
        obs, reward, done, info = env_instance.step({"action": act_val})
        return {
            "observation": obs,
            "reward": float(reward),
            "done": bool(done),
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/baseline")
def baseline():
    scores = []
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        obs = env_instance.reset(task)
        email = obs["email_text"].lower()

        # simple agent
        if "refund" in email:
            action = "refund"
        elif any(k in email for k in ["help", "issue", "problem", "angry"]):
            action = "support"
        else:
            action = "ignore"

        obs, reward, done, info = env_instance.step({"action": action})
        score = env_instance.grader(action)
        scores.append(score)

    return {
        "baseline_score": sum(scores)/len(scores),
        "task_scores": scores
    }

@app.post("/grader")
def grader(action: dict):
    act_val = action.get("action", action)
    score = env_instance.grader(act_val)
    return {"score": float(score)}

@app.get("/state")
def state():
    return env_instance.state()

@app.get("/health")
def health():
    return {"status": "ok"}