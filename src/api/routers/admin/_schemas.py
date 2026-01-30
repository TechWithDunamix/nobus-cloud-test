from ninja import Schema
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from api.routers.loans._schemas import LoanApplicationResponse

class LoanStatusUpdate(Schema):
    status: str = Field(..., pattern="^(APPROVED|REJECTED)$", description="New status for the loan")
    reason: Optional[str] = Field(None, description="Reason for the status change")

class AdminLogResponse(Schema):
    id: int
    admin_id: int
    action: str
    target_id: int
    target_model: str
    details: Optional[str]
    created_at: datetime
