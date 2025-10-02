from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Expense(BaseModel):
    """Schema for expense records"""
    date: datetime = Field(..., description="Date of the expense")
    category: str = Field(..., description="Category of the expense (e.g., food, transport, utilities)")
    description: str = Field(..., description="Description of the expense")
    amount: float = Field(..., gt=0, description="Amount of the expense")
    payment_method: str = Field(..., description="Payment method used (e.g., cash, credit card, debit card)")
    vendor: str = Field(..., description="Vendor or merchant name")
    embedding: Optional[list[float]] = Field(None, description="Vector embedding for semantic search")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-10-02T10:30:00",
                "category": "food",
                "description": "Lunch at downtown restaurant",
                "amount": 25.50,
                "payment_method": "credit card",
                "vendor": "The Bistro",
                "embedding": None
            }
        }
