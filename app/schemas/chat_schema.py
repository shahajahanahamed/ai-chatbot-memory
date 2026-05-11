from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=5,
        description="User query cannot be less than 5 characters",
        examples=["What is AI?"]
    )
    user_id: int = Field(
        ...,
        ge=1,
        description="User ID must be a positive integer",
        examples=[123]
    )


class ChatResponse(BaseModel):
    can_answer: bool = Field(
        ...,
        description="Indicates whether the system can answer the query"
    )
    actual_answer: str = Field(
        ...,
        min_length=1,
        description="Actual answer to the query"
    )