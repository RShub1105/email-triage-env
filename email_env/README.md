# 📧 Email Triage OpenEnv Environment

## 🚀 Overview

This project implements a **real-world OpenEnv environment** for **email triaging**, where an AI agent learns to classify incoming customer emails into appropriate actions.

The environment follows the standard OpenEnv API:

* `reset()`
* `step()`
* `state()`

It is designed to simulate real customer support workflows used in:

* Helpdesk systems
* Customer support automation
* AI assistants

---

## 🧠 Why This Matters

Email triaging is a **real-world, high-impact problem**:

* Companies receive thousands of support emails daily
* Manual classification is slow and expensive
* AI agents must handle:

  * Ambiguous requests
  * Emotional tone
  * Multi-intent queries

👉 This environment helps evaluate how well AI systems handle these challenges.

---

## 🖼️ Environment Flow

---

## 🎯 Tasks (Difficulty Levels)

The environment includes **3 progressively difficult tasks**:

### 🟢 Easy

* Clear intent emails
* Example: *"I want a refund for my order"*

### 🟡 Medium

* Mixed or multi-intent emails
* Example: *"I need a refund and help logging in"*

### 🔴 Hard

* Emotional or ambiguous emails
* Example: *"This is frustrating, fix this now!"*

---

## ⚙️ Action Space

The agent must choose one action:

```json
{
  "action": "refund | support | ignore"
}
```

---

## 👀 Observation Space

The environment returns:

```json
{
  "email_text": "Customer email content"
}
```

---

## 🎁 Reward Function

The reward system provides **dense feedback**:

* ✅ Correct action → `+1.0`
* ⚠️ Partially correct → `+0.3`
* ❌ Wrong action → `-0.5`

👉 This encourages learning and avoids sparse rewards.

---

## 🧪 API Endpoints

| Endpoint    | Description        |
| ----------- | ------------------ |
| `/reset`    | Start new task     |
| `/step`     | Take action        |
| `/state`    | Get current state  |
| `/tasks`    | List tasks         |
| `/grader`   | Score performance  |
| `/baseline` | Run baseline agent |

---

## 🖥️ Running Locally

```bash
uvicorn email_env.server.app:app --reload
```

Open:
👉 http://127.0.0.1:8000/docs

---

## 🐳 Run with Docker

```bash
docker build -t email-env .
docker run -p 7860:7860 email-env
```

Open:
👉 http://localhost:7860/docs

---

## 🤖 Baseline Agent

A simple rule-based agent is provided:

* Detects keywords like "refund", "help", "issue"
* Produces reproducible baseline scores

Example output:

```json
{
  "baseline_score": 0.83,
  "task_scores": [1.0, 0.5, 1.0]
}
```

---

## 📊 Evaluation Design

This environment is designed for:

* Reinforcement Learning (RL)
* LLM Agent Evaluation
* Decision-making systems

It tests:

* Intent understanding
* Robustness to ambiguity
* Handling emotional language

---

## 🏗️ Tech Stack

* FastAPI
* Python
* Docker
* OpenEnv Specification

---

## 🌍 Deployment

Deployed on Hugging Face Spaces using Docker.

---

## Baseline Inference

Run the baseline agent:

```bash
python baseline.py

## 💡 Future Improvements

* Add multi-step conversations
* Introduce priority levels
* Integrate LLM-based grading
* Expand action space (escalation, tagging, etc.)

---

## 🏆 Hackathon Submission

Built for OpenEnv Hackathon Round 1.

Focus areas:

* Real-world utility ✅
* Task design ✅
* Reward shaping ✅
* Deployment ✅

---

## 🙌 Author

Rahul Sharma

---

## ⭐ If you like this project

Give it a star ⭐ and share feedback!
