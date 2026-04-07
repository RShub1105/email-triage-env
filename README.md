# 📧 Email Triage Environment (OpenEnv RL Challenge)

An interactive reinforcement learning environment for **email classification and triage**, built for the OpenEnv Hackathon.
The agent must classify incoming emails into one of three categories:

* **refund**
* **support**
* **ignore**

---

## 🚀 Project Overview

This project simulates a real-world customer support system where an AI agent processes emails and decides the correct action. The environment provides:

* Task-based evaluation (`easy`, `medium`, `hard`)
* Step-by-step interaction (`reset → step → grader`)
* Scoring mechanism for agent performance

---

## 🧠 How It Works

1. **Reset Environment**

   * Initializes a new task and returns an email

2. **Agent Inference**

   * The agent reads the email and predicts an action

3. **Step Execution**

   * The environment processes the action

4. **Grading**

   * Returns a score based on correctness

---

## 📂 Project Structure

```
email-triage-env/
├── server/
│   ├── app.py          # FastAPI server (OpenEnv endpoints)
│   ├── client.py       # Environment logic
│   └── models.py       # Data models
├── inference.py        # Agent script (LLM-based)
├── Dockerfile          # Container setup
├── pyproject.toml      # Project config
├── requirements.txt    # Dependencies
├── openenv.yaml        # OpenEnv metadata
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```
git clone https://github.com/RShub1105/email-triage-env.git
cd email-triage-env
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Run the server

```
python -m server.app
```

Server will start at:

```
http://localhost:7860
```

---

## 🔌 API Endpoints

| Endpoint  | Method | Description         |
| --------- | ------ | ------------------- |
| `/reset`  | POST   | Start a new task    |
| `/step`   | POST   | Take an action      |
| `/grader` | POST   | Get score           |
| `/health` | GET    | Check server status |

---

## 🤖 Inference (Agent)

The agent uses the **OpenAI client** (via Hugging Face router) to classify emails.

### Required Environment Variables

```
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=meta-llama/Llama-3-8b-instruct
HF_TOKEN=your_token_here
```

---

### Run Inference

```
python inference.py
```

---

## 🐳 Docker Support

Build and run using Docker:

```
docker build -t email-env .
docker run -p 7860:7860 email-env
```

---

## 🧪 Example Workflow

```
POST /reset → get email
POST /step → send action
POST /grader → receive score
```

---

## 📊 Evaluation

The agent is evaluated across:

* Easy
* Medium
* Hard tasks

Final score = average across all tasks

---

## 🛠 Tech Stack

* **FastAPI** — API server
* **OpenAI Python SDK** — LLM inference
* **Docker** — containerization
* **OpenEnv** — evaluation framework

---

## 📌 Notes

* Designed to run within:

  * 2 vCPU
  * 8 GB RAM
* Hugging Face Space must be in **Running** state before submission

---

## 🙌 Acknowledgements

Built for the **OpenEnv RL Hackathon**
Special thanks to the organizers and support team.

---

## 📬 Contact

For issues or questions, feel free to reach out or open an issue in the repository.

---

⭐ If you found this helpful, consider giving the repo a star!
