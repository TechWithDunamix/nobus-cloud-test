from pydantic import BaseModel, EmailStr, Field, constr

Username = constr(min_length=3, max_length=50)
SecurePassword = constr(min_length=8)

class Register(BaseModel):
    full_name: Username = Field(..., description="Your official full designation")
    password: SecurePassword = Field(..., description="Must be top-secret and strong")
    email: EmailStr = Field(..., description="Electronic mail identifier")
