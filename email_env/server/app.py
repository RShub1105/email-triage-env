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
        try:
            local_env = EmailEnv()

            obs = local_env.reset(task)

            if not isinstance(obs, dict) or "email_text" not in obs:
                return {"error": f"Invalid observation for {task}"}

            email = str(obs["email_text"]).lower()

            # agent logic
            if "refund" in email:
                action = "refund"
            elif any(k in email for k in ["help", "issue", "problem"]):
                action = "support"
            elif any(k in email for k in ["frustrating", "angry"]):
                action = "support"
            else:
                action = "ignore"

            # step safely
            step_result = local_env.step({"action": action})

            if not isinstance(step_result, tuple) or len(step_result) != 4:
                scores.append(0.0)
                continue

            _, reward, _, _ = step_result

            # grader safely
            try:
                score = float(local_env.grader(action))
            except:
                score = 0.0

            scores.append(score)

        except Exception as e:
            print(f"Baseline error on {task}: {e}")  # logs only
            scores.append(0.0)

    return {
        "baseline_score": float(sum(scores) / len(scores)) if scores else 0.0,
        "task_scores": [float(s) for s in scores]
    }

@app.get("/state")
def state():
    return env.state()

@app.get("/health")
def health():
    return {"status": "ok"}