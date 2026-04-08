import os
import requests
from openai import OpenAI

# 1. Setup Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")

# Check for API Key but don't crash immediately if you want the validator to see the start
if not API_KEY:
    print("[ERROR] HF_TOKEN is missing!", flush=True)
    # We leave this check here to help you debug locally
    raise ValueError("HF_TOKEN or OPENAI_API_KEY environment variable is required")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-8b-instruct")
ENV_URL = "http://localhost:7860"

def get_agent_action(email_text):
    if not email_text:
        return "ignore"
    prompt = f"Classify this email as 'refund', 'support', or 'ignore'. Email: {email_text}\nRespond ONLY with the word."
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            timeout=20
        )
        prediction = response.choices[0].message.content.strip().lower() # pyright: ignore[reportOptionalMemberAccess]
        return prediction if prediction in ["refund", "support", "ignore"] else "ignore"
    except Exception as e:
        print(f"[ERROR] LLM Inference failed: {e}", flush=True)
        return "ignore"

def main():
    tasks = ["easy", "medium", "hard"]
    total_score = 0

    for task in tasks:
        print(f"[START] task={task}", flush=True)
        
        # FIX: Define default values so the script doesn't crash if requests fail
        action = "ignore"
        score = 0
        
        try:
            # 1. Reset
            res = requests.post(f"{ENV_URL}/reset", params={"task": task}, timeout=10).json()
            email = res.get("observation", {}).get("email_text", "")

            # 2. Predict
            action = get_agent_action(email)
            print(f"[STEP] step=1 action={action}", flush=True)

            # 3. Submit & Grade
            requests.post(f"{ENV_URL}/step", json={"action": action}, timeout=10)
            grade_res = requests.post(f"{ENV_URL}/grader", json={"action": action}, timeout=10).json()
            score = grade_res.get("score", 0)

        except Exception as e:
            print(f"[ERROR] Task {task} encountered an issue: {e}", flush=True)

        # Always print END even if the try block failed
        print(f"[END] task={task} score={score} steps=1", flush=True)
        total_score += score

    avg_score = total_score / len(tasks)
    print(f"[FINAL] average_score={avg_score}", flush=True)

if __name__ == "__main__":
    main()