import json
from ninja import Router
from ninja.errors import HttpError
from typing import List
from django.db import transaction
from api.models.loan_application import LoanApplication, LoanStatus
from api.models.admin_log import AdminLog
from api.models.user import User
from api.services.auth_service import AuthBearer
from ._schemas import LoanStatusUpdate, AdminLogResponse
from api.routers.loans._schemas import LoanApplicationResponse

router = Router(tags=["Admin"])

class AdminAuth(AuthBearer):
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        if user and user.is_staff:
            return user
        return None

@router.get("/loans", response=List[LoanApplicationResponse], auth=AdminAuth(), summary="List all loan applications")
def list_all_loans(request):
    """
    List all loan applications (Admin only).
    """
    return LoanApplication.objects.all().order_by('-created_at')

@router.put("/loans/{loan_id}/status", response=LoanApplicationResponse, auth=AdminAuth(), summary="Approve or Reject a loan")
def update_loan_status(request, loan_id: int, payload: LoanStatusUpdate):
    """
    Approve or Reject a loan application.
    This action is logged in AdminLog.
    """
    with transaction.atomic():
        try:
            loan = LoanApplication.objects.get(id=loan_id)
        except LoanApplication.DoesNotExist:
            raise HttpError(404, "Loan not found")
            
        if loan.status != LoanStatus.PENDING:
            raise HttpError(400, f"Loan is already {loan.status}")
            
        loan.status = payload.status
        loan.save()
        
        # Audit Log
        AdminLog.objects.create(
            admin=request.auth,
            action=f"{payload.status}_LOAN",
            target_id=loan.id,
            target_model="LoanApplication",
            details=json.dumps({"reason": payload.reason}) if payload.reason else ""
        )
        
        return loan

@router.get("/logs", response=List[AdminLogResponse], auth=AdminAuth(), summary="View admin logs")
def list_admin_logs(request):
    """
    View audit logs of admin actions.
    """
    return AdminLog.objects.all().order_by('-created_at')
