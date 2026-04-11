from typing import Literal

from pydantic import BaseModel, Field


class EmailObservation(BaseModel):
    email_id: str = Field(description="Unique scenario identifier for reproducibility.")
    subject: str
    sender: str
    customer_tier: Literal["unknown", "standard", "gold", "platinum"]
    sla_hours_remaining: int
    email_text: str
    thread_history: list[str]
    order_status: str
    allowed_actions: list[Literal["refund", "support", "ignore"]]
    task: Literal["easy", "medium", "hard"]


class EmailAction(BaseModel):
    action: Literal["refund", "support", "ignore"] = Field(
        description="Choose the next triage queue for the incoming email."
    )


class EmailReward(BaseModel):
    reward: float = Field(ge=0.0, le=1.0)
    score: float = Field(ge=0.0, le=1.0)
    done: bool
    last_action_error: str | None = None
