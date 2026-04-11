from __future__ import annotations

from copy import deepcopy
from typing import Any


VALID_ACTIONS = {"refund", "support", "ignore"}


SCENARIOS: dict[str, list[dict[str, Any]]] = {
    "easy": [
        {
            "id": "easy_refund_damaged_item",
            "subject": "Refund request for damaged blender",
            "sender": "maya.patel@example.com",
            "customer_tier": "standard",
            "sla_hours_remaining": 18,
            "email_text": (
                "Hi team, my blender arrived with a cracked jar and I would like a full refund. "
                "Order #1842 was delivered this morning."
            ),
            "thread_history": [
                "Customer placed order three days ago.",
                "Courier marked parcel as delivered at 9:12 AM.",
            ],
            "order_status": "delivered_damaged",
            "expected_action": "refund",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Customer explicitly requests money back for a damaged item.",
        },
        {
            "id": "easy_support_password_reset",
            "subject": "Locked out after password reset",
            "sender": "aditya.verma@example.com",
            "customer_tier": "standard",
            "sla_hours_remaining": 10,
            "email_text": (
                "Hello, I reset my password but I still cannot sign in to my account. "
                "Can someone help me regain access?"
            ),
            "thread_history": [
                "No prior refund history.",
                "User successfully passed identity verification last month.",
            ],
            "order_status": "not_applicable",
            "expected_action": "support",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Access issue with a direct support request.",
        },
        {
            "id": "easy_ignore_marketing_opt_in",
            "subject": "Collaboration inquiry",
            "sender": "promo@partner-campaigns.biz",
            "customer_tier": "unknown",
            "sla_hours_remaining": 72,
            "email_text": (
                "We help brands scale awareness. Reply if you want our media kit and sponsorship rates."
            ),
            "thread_history": [
                "No matching customer account.",
                "Similar messages have been classified as non-support outreach.",
            ],
            "order_status": "not_applicable",
            "expected_action": "ignore",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Not a customer support or refund request.",
        },
    ],
    "medium": [
        {
            "id": "medium_duplicate_charge",
            "subject": "Charged twice for one order",
            "sender": "nisha.rao@example.com",
            "customer_tier": "gold",
            "sla_hours_remaining": 6,
            "email_text": (
                "I can see two charges for the same order on my card statement. "
                "Please reverse the duplicate payment as soon as possible."
            ),
            "thread_history": [
                "Billing system shows one successful order and one duplicate capture pending settlement.",
                "Customer has had no previous disputes.",
            ],
            "order_status": "billing_dispute",
            "expected_action": "refund",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Financial correction is the primary next step.",
        },
        {
            "id": "medium_replacement_status",
            "subject": "Replacement still not delivered",
            "sender": "samir.khan@example.com",
            "customer_tier": "standard",
            "sla_hours_remaining": 8,
            "email_text": (
                "My replacement headphones were supposed to arrive yesterday but tracking has not moved. "
                "Can you check what is happening?"
            ),
            "thread_history": [
                "Original unit was already approved for replacement.",
                "Customer is asking for an update, not a refund.",
            ],
            "order_status": "replacement_in_transit",
            "expected_action": "support",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Needs operational investigation and customer communication.",
        },
        {
            "id": "medium_vendor_pitch",
            "subject": "Can we sell through your marketplace?",
            "sender": "bizdev@wholesale-fast.io",
            "customer_tier": "unknown",
            "sla_hours_remaining": 96,
            "email_text": (
                "We are a wholesaler looking for a distribution partnership. "
                "Please connect us with your procurement team."
            ),
            "thread_history": [
                "No customer order tied to this sender.",
                "Mailbox policy says business development outreach should not enter support queues.",
            ],
            "order_status": "not_applicable",
            "expected_action": "ignore",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Legitimate email but outside support scope.",
        },
    ],
    "hard": [
        {
            "id": "hard_damaged_and_locked_out",
            "subject": "Damaged order and account access issue",
            "sender": "riya.shah@example.com",
            "customer_tier": "platinum",
            "sla_hours_remaining": 3,
            "email_text": (
                "I received a broken coffee machine and I also cannot log in to upload photos. "
                "I mainly want my money back today because this was a gift."
            ),
            "thread_history": [
                "High-value customer with two past purchases and no prior claims.",
                "Policy says explicit refund intent takes priority when item is damaged on arrival.",
            ],
            "order_status": "delivered_damaged",
            "expected_action": "refund",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Mixed-signal email where refund intent outweighs support need.",
        },
        {
            "id": "hard_angry_but_fixable",
            "subject": "Nothing works and this is getting ridiculous",
            "sender": "kabir.mehra@example.com",
            "customer_tier": "gold",
            "sla_hours_remaining": 4,
            "email_text": (
                "Your service has been frustrating all week. My premium account keeps logging out and the export page crashes. "
                "I need someone competent to sort this out."
            ),
            "thread_history": [
                "No billing dispute or cancellation recorded.",
                "Product telemetry shows repeated session expiry errors on the export page.",
            ],
            "order_status": "service_incident",
            "expected_action": "support",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Angry tone should not be mistaken for a refund request.",
        },
        {
            "id": "hard_cancellation_language",
            "subject": "Cancel everything",
            "sender": "tanvi.gupta@example.com",
            "customer_tier": "standard",
            "sla_hours_remaining": 5,
            "email_text": (
                "I am extremely disappointed. My package never arrived and I do not want another shipment. "
                "Cancel the order and return my payment."
            ),
            "thread_history": [
                "Carrier scan shows parcel lost in transit.",
                "Customer explicitly rejects replacement and requests payment reversal.",
            ],
            "order_status": "lost_in_transit",
            "expected_action": "refund",
            "allowed_actions": ["refund", "support", "ignore"],
            "notes": "Cancellation language plus lost shipment resolves to refund.",
        },
    ],
}


PARTIAL_CREDIT: dict[tuple[str, str], float] = {
    ("refund", "support"): 0.55,
    ("support", "refund"): 0.4,
    ("support", "ignore"): 0.15,
    ("refund", "ignore"): 0.1,
    ("ignore", "support"): 0.1,
    ("ignore", "refund"): 0.05,
}


class EmailEnv:
    def __init__(self) -> None:
        self.tasks = SCENARIOS
        self._task_offsets = {task_name: 0 for task_name in self.tasks}
        self.current_task = "easy"
        self.current_scenario: dict[str, Any] | None = None
        self.last_action: str | None = None
        self.last_action_error: str | None = None
        self.last_reward = 0.0
        self.last_score = 0.0
        self.steps_taken = 0

    def reset(self, task: str = "easy") -> dict[str, Any]:
        if task not in self.tasks:
            raise ValueError(f"Unknown task '{task}'. Expected one of: {', '.join(sorted(self.tasks))}")

        scenarios = self.tasks[task]
        index = self._task_offsets[task] % len(scenarios)
        self._task_offsets[task] += 1

        self.current_task = task
        self.current_scenario = deepcopy(scenarios[index])
        self.last_action = None
        self.last_action_error = None
        self.last_reward = 0.0
        self.last_score = 0.0
        self.steps_taken = 0
        return self._build_observation()

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool, dict[str, Any]]:
        if not self.current_scenario:
            raise ValueError("Environment must be reset before calling step().")

        predicted = str(action.get("action", "")).strip().lower()
        self.steps_taken += 1
        self.last_action = predicted

        if predicted not in VALID_ACTIONS:
            self.last_action_error = (
                f"Invalid action '{predicted}'. Allowed actions: {', '.join(sorted(VALID_ACTIONS))}"
            )
            self.last_reward = 0.0
            self.last_score = 0.0
            info = {
                "expected_action": self.current_scenario["expected_action"],
                "last_action_error": self.last_action_error,
                "score": self.last_score,
                "scenario_id": self.current_scenario["id"],
            }
            return self._build_observation(), self.last_reward, True, info

        self.last_action_error = None
        self.last_score = self._score_action(predicted)
        self.last_reward = self._reward_action(predicted)
        info = {
            "expected_action": self.current_scenario["expected_action"],
            "last_action_error": None,
            "score": self.last_score,
            "scenario_id": self.current_scenario["id"],
        }
        return self._build_observation(), self.last_reward, True, info

    def grader(self, action: str) -> float:
        if not self.current_scenario:
            raise ValueError("Environment must be reset before calling grader().")
        return self._score_action(str(action).strip().lower())

    def state(self) -> dict[str, Any]:
        return {
            "task": self.current_task,
            "steps_taken": self.steps_taken,
            "current_scenario": self.current_scenario,
            "last_action": self.last_action,
            "last_reward": self.last_reward,
            "last_score": self.last_score,
            "last_action_error": self.last_action_error,
        }

    def smart_classify(self, email: str) -> str:
        email_lower = email.lower()

        refund_terms = ["refund", "money back", "charged twice", "return my payment", "cancel the order"]
        support_terms = ["help", "cannot log in", "can't log in", "reset my password", "check what is happening"]

        if any(term in email_lower for term in refund_terms):
            return "refund"
        if any(term in email_lower for term in support_terms):
            return "support"
        return "ignore"

    def _build_observation(self) -> dict[str, Any]:
        if not self.current_scenario:
            raise ValueError("Environment has no active scenario.")

        scenario = self.current_scenario
        return {
            "email_id": scenario["id"],
            "subject": scenario["subject"],
            "sender": scenario["sender"],
            "customer_tier": scenario["customer_tier"],
            "sla_hours_remaining": scenario["sla_hours_remaining"],
            "email_text": scenario["email_text"],
            "thread_history": list(scenario["thread_history"]),
            "order_status": scenario["order_status"],
            "allowed_actions": list(scenario["allowed_actions"]),
            "task": self.current_task,
        }

    def _score_action(self, predicted: str) -> float: 
        expected = self.current_scenario["expected_action"]
        if predicted == expected:
            return 0.99  
        partial = PARTIAL_CREDIT.get((expected, predicted), 0.1)
        return max(0.05, min(0.95, partial))

    def _reward_action(self, predicted: str) -> float:
        score = self._score_action(predicted)
        scenario = self.current_scenario
        urgency_bonus = 0.0

        if predicted == scenario["expected_action"] and scenario["sla_hours_remaining"] <= 6:
            urgency_bonus = 0.05
        elif predicted == "ignore" and scenario["expected_action"] != "ignore":
            urgency_bonus = -0.05

        reward = max(0.0, min(1.0, score * 0.9 + urgency_bonus))
        return round(reward, 2)
