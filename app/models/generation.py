"""Generation data model."""

from datetime import datetime

from pydantic import BaseModel, Field


class Generation(BaseModel):
    """Generation record model."""

    id: str = Field(..., description="Unique generation ID")
    content: str = Field(..., description="Generation content")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "gen-123",
                "content": "Generated content",
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "model": "gpt-4",
                },
            }
        }