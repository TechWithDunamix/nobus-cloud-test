"""
JWT Token Service

This service handles JWT token creation and validation for authentication.
Supports both access tokens (short-lived) and refresh tokens (long-lived).
"""

import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from django.conf import settings


class JWTService:
    """Service for creating and validating JWT tokens."""
    
    @staticmethod
    def _get_secret_key() -> str:
        """Get the JWT secret key from settings."""
        return getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
    
    @staticmethod
    def _get_algorithm() -> str:
        """Get the JWT algorithm from settings."""
        return getattr(settings, 'JWT_ALGORITHM', 'HS256')
    
    @staticmethod
    def _get_access_token_lifetime() -> timedelta:
        """Get the access token lifetime from settings."""
        minutes = getattr(settings, 'JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 15)
        return timedelta(minutes=minutes)
    
    @staticmethod
    def _get_refresh_token_lifetime() -> timedelta:
        """Get the refresh token lifetime from settings."""
        days = getattr(settings, 'JWT_REFRESH_TOKEN_LIFETIME_DAYS', 7)
        return timedelta(days=days)
    
    @classmethod
    def create_access_token(cls, user_id: int, email: str, **extra_claims) -> str:
        """
        Create a JWT access token.
        
        Args:
            user_id: The user's ID
            email: The user's email
            **extra_claims: Additional claims to include in the token
            
        Returns:
            str: The encoded JWT access token
        """
        now = datetime.utcnow()
        expiration = now + cls._get_access_token_lifetime()
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'iat': now,
            'exp': expiration,
            **extra_claims
        }
        
        token = jwt.encode(
            payload,
            cls._get_secret_key(),
            algorithm=cls._get_algorithm()
        )
        
        return token
    
    @classmethod
    def create_refresh_token(cls, user_id: int, email: str, **extra_claims) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            user_id: The user's ID
            email: The user's email
            **extra_claims: Additional claims to include in the token
            
        Returns:
            str: The encoded JWT refresh token
        """
        now = datetime.utcnow()
        expiration = now + cls._get_refresh_token_lifetime()
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'refresh',
            'iat': now,
            'exp': expiration,
            **extra_claims
        }
        
        token = jwt.encode(
            payload,
            cls._get_secret_key(),
            algorithm=cls._get_algorithm()
        )
        
        return token
    
    @classmethod
    def create_token_pair(cls, user_id: int, email: str, **extra_claims) -> Dict[str, str]:
        """
        Create both access and refresh tokens.
        
        Args:
            user_id: The user's ID
            email: The user's email
            **extra_claims: Additional claims to include in both tokens
            
        Returns:
            dict: A dictionary containing 'access' and 'refresh' tokens
        """
        return {
            'access': cls.create_access_token(user_id, email, **extra_claims),
            'refresh': cls.create_refresh_token(user_id, email, **extra_claims)
        }
    
    @classmethod
    def validate_token(cls, token: str, expected_type: Optional[str] = None) -> Dict:
        """
        Validate and decode a JWT token.
        
        Args:
            token: The JWT token to validate
            expected_type: Optional token type to verify ('access' or 'refresh')
            
        Returns:
            dict: The decoded token payload
            
        Raises:
            jwt.ExpiredSignatureError: If the token has expired
            jwt.InvalidTokenError: If the token is invalid
            ValueError: If the token type doesn't match expected_type
        """
        try:
            payload = jwt.decode(
                token,
                cls._get_secret_key(),
                algorithms=[cls._get_algorithm()]
            )
            
            # Verify token type if specified
            if expected_type and payload.get('type') != expected_type:
                raise ValueError(
                    f"Invalid token type. Expected '{expected_type}', "
                    f"got '{payload.get('type')}'"
                )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid token: {str(e)}")
    
    @classmethod
    def validate_access_token(cls, token: str) -> Dict:
        """
        Validate an access token.
        
        Args:
            token: The JWT access token to validate
            
        Returns:
            dict: The decoded token payload
            
        Raises:
            jwt.ExpiredSignatureError: If the token has expired
            jwt.InvalidTokenError: If the token is invalid
            ValueError: If the token is not an access token
        """
        return cls.validate_token(token, expected_type='access')
    
    @classmethod
    def validate_refresh_token(cls, token: str) -> Dict:
        """
        Validate a refresh token.
        
        Args:
            token: The JWT refresh token to validate
            
        Returns:
            dict: The decoded token payload
            
        Raises:
            jwt.ExpiredSignatureError: If the token has expired
            jwt.InvalidTokenError: If the token is invalid
            ValueError: If the token is not a refresh token
        """
        return cls.validate_token(token, expected_type='refresh')
    
    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> Tuple[str, Dict]:
        """
        Generate a new access token using a refresh token.
        
        Args:
            refresh_token: The JWT refresh token
            
        Returns:
            tuple: A tuple containing (new_access_token, payload)
            
        Raises:
            jwt.ExpiredSignatureError: If the refresh token has expired
            jwt.InvalidTokenError: If the refresh token is invalid
            ValueError: If the token is not a refresh token
        """
        payload = cls.validate_refresh_token(refresh_token)
        
        # Create a new access token with the same user information
        new_access_token = cls.create_access_token(
            user_id=payload['user_id'],
            email=payload['email']
        )
        
        return new_access_token, payload
    
    @classmethod
    def decode_token_without_validation(cls, token: str) -> Optional[Dict]:
        """
        Decode a token without validating its signature or expiration.
        Useful for inspecting expired tokens or debugging.
        
        Args:
            token: The JWT token to decode
            
        Returns:
            dict: The decoded token payload, or None if decoding fails
        """
        try:
            return jwt.decode(
                token,
                options={"verify_signature": False, "verify_exp": False}
            )
        except Exception:
            return None
