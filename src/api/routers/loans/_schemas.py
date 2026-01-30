from ninja import Schema
from pydantic import Field
from datetime import datetime

class LoanApplicationCreate(Schema):
    amount: float = Field(..., gt=0, description="Loan amount requested")
    tenure_months: int = Field(..., gt=0, description="Tenure in months")
    purpose: str = Field(..., min_length=5, description="Purpose of the loan")

class LoanApplicationResponse(Schema):
    id: int
    user_id: int
    amount: float
    tenure_months: int
    purpose: str
    status: str
    created_at: datetime
