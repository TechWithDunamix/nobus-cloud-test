from ninja import Router
from typing import List
from api.models.loan_application import LoanApplication
from api.services.auth_service import AuthBearer
from ._schemas import LoanApplicationCreate, LoanApplicationResponse

router = Router(tags=["Loans"])

@router.post("/", response=LoanApplicationResponse, auth=AuthBearer(), summary="Create a loan application")
def create_loan_application(request, payload: LoanApplicationCreate):
    """
    Create a new loan application.
    The default status will be PENDING.
    """
    loan = LoanApplication.objects.create(
        user=request.auth,
        amount=payload.amount,
        tenure_months=payload.tenure_months,
        purpose=payload.purpose
    )
    return loan

@router.get("/", response=List[LoanApplicationResponse], auth=AuthBearer(), summary="List my loan applications")
def list_loan_applications(request):
    """
    List all loan applications for the authenticated user.
    """
    return LoanApplication.objects.filter(user=request.auth).all()

@router.get("/{loan_id}", response=LoanApplicationResponse, auth=AuthBearer(), summary="Get loan application details")
def get_loan_application(request, loan_id: int):
    """
    Get details of a specific loan application.
    Only the owner can view it.
    """
    return LoanApplication.objects.get(id=loan_id, user=request.auth)
