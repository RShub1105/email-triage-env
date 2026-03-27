from pydantic import BaseModel

class EmailObservation(BaseModel):
    email_text: str


class EmailAction(BaseModel):
    action: str  # "refund", "support", "ignore"