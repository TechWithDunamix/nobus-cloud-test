from pydantic import BaseModel, EmailStr, Field, constr

Username = constr(min_length=3, max_length=50)
SecurePassword = constr(min_length=8)

class Register(BaseModel):
    full_name: Username = Field(..., description="Your official full designation")
    password: SecurePassword = Field(..., description="Must be top-secret and strong")
    email: EmailStr = Field(..., description="Electronic mail identifier")

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email for login")
    password: SecurePassword = Field(..., description="User password")

class TokenResponse(BaseModel):
    access: str = Field(..., description="JWT Access Token")
    refresh: str = Field(..., description="JWT Refresh Token")

class RefreshTokenRequest(BaseModel):
    refresh: str = Field(..., description="Refresh Token to get new access token")
