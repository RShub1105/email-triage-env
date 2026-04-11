---
title: Email Triage Env
emoji: "📧"
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "latest"
app_file: email_env/server/app.py
pinned: false
---

# Email Triage Environment

`email-triage-env` is a compact OpenEnv benchmark for a real support-operations task: triaging customer emails into the correct queue. The environment models the kind of decisions an ops agent makes every day, where the message content, thread history, customer tier, and SLA pressure all matter.

The environment is intentionally deterministic and lightweight so it can run cleanly inside the hackathon constraints, while still giving reviewers a realistic benchmark instead of a toy classifier.

## Why this is a real-world task

Support teams routinely need to decide whether an incoming email should:

- go straight to a refund queue,
- go to a support/investigation queue, or
- be ignored because it is outside the support workflow.

That routing decision affects response time, chargeback risk, queue health, and customer satisfaction. The benchmark reflects those tradeoffs with scenario metadata like `customer_tier`, `order_status`, `thread_history`, and `sla_hours_remaining`.

## Environment API

The server exposes the standard hackathon-friendly HTTP surface:

- `POST /reset?task=<easy|medium|hard>`
- `POST /step`
- `POST /grader`
- `GET /state`
- `GET /health`

## Observation Space

`/reset` returns an observation object with:

- `email_id`: deterministic scenario identifier
- `subject`: email subject line
- `sender`: customer or sender address
- `customer_tier`: `unknown | standard | gold | platinum`
- `sla_hours_remaining`: remaining SLA time
- `email_text`: main email content
- `thread_history`: prior context and policy hints
- `order_status`: business status for the case
- `allowed_actions`: valid action strings
- `task`: current difficulty bucket

## Action Space

The action space is intentionally small and typed:

- `refund`
- `support`
- `ignore`

The agent should choose the queue that best matches the customer’s primary requested outcome.

## Task Design

The benchmark includes three difficulty levels with deterministic scenario rotation:

- `easy`: direct single-intent emails
- `medium`: more realistic cases with billing/logistics nuance
- `hard`: ambiguous or mixed-intent emails where the agent must prioritize correctly

Examples of difficult behavior:

- angry customers who need support, not refunds
- mixed refund + access issues where refund intent should dominate
- irrelevant business outreach that should stay out of support queues

## Reward Design

The grader returns a deterministic score in `[0.0, 1.0]`.

- `1.0` for the correct queue
- partial credit for business-plausible but suboptimal routing
- `0.0` for clearly wrong handling

The step reward is also normalized to `[0.0, 1.0]` and is shaped from:

- grader score
- urgency bonus for correctly handling high-SLA-risk emails
- small penalty for ignoring emails that clearly need action

This gives denser learning signal than a purely binary reward.

## Baseline Inference

The root `inference.py` uses the OpenAI Python client as required by the hackathon and emits stdout in the required:

- `[START]`
- `[STEP]`
- `[END]`

format.

Required environment variables:

```bash
export API_BASE_URL="https://your-validator-proxy/v1"
export API_KEY="your_validator_key"
export MODEL_NAME="meta-llama/Llama-3-8b-instruct"
```

Run the local server:

```bash
python -m email_env.server.app
```

Run inference:

```bash
python inference.py
```

## Local Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
python -m email_env.server.app
```

Health check:

```bash
curl http://localhost:7860/health
```

## Docker

Build:

```bash
docker build -t email-triage-env .
```

Run:

```bash
docker run -p 7860:7860 email-triage-env
```

## Submission Notes

This project is designed for the OpenEnv Round 1 constraints:

- reproducible scenario order
- deterministic grader
- 3 difficulty levels
- normalized reward/score outputs
- lightweight runtime for `2 vCPU / 8 GB RAM`
