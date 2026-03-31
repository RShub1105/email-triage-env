import os
import json
import requests
from openai import OpenAI

# Required Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-8b-instruct") # Example fallback
ENV_URL = "http://localhost:7860" # In prod, this points to your HF Space

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def get_agent_action(email_text):
    prompt = f"""
    You are a customer support triage assistant. 
    Classify the following email into exactly one category: "refund", "support", or "ignore".
    
    Email: {email_text}
    
    Respond with ONLY the word of the category.
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message.content
    return content.strip().lower() if content else ""

def main():
    tasks = ["easy", "medium", "hard"]
    total_score = 0

    for task in tasks:
        # 1. Reset
        res = requests.post(f"{ENV_URL}/reset", params={"task": task}).json()
        email = res["observation"]["email_text"]

        # 2. Inference
        action = get_agent_action(email)
        
        # 3. Step
        step_res = requests.post(f"{ENV_URL}/step", json={"action": action}).json()
        
        # 4. Grade
        grade_res = requests.post(f"{ENV_URL}/grader", json={"action": action}).json()
        score = grade_res["score"]
        
        print(f"Task: {task} | Action: {action} | Score: {score}")
        total_score += score

    print(f"\nFINAL AVG SCORE: {total_score / len(tasks)}")

if __name__ == "__main__":
    main()