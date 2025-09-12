"""
Pydantic Schemas for Periodic Table Web App
Request and response validation models for API endpoints

This file defines the data structures used for API requests and responses
using Pydantic for automatic validation and serialization
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class ElementBase(BaseModel):
    """
    Base schema for element data
    Contains the common fields shared across all element operations
    """
    symbol: str = Field(..., min_length=1, max_length=10, description="Chemical symbol (e.g., 'H', 'He')")
    name: str = Field(..., min_length=1, max_length=50, description="Full element name (e.g., 'Hydrogen')")
    number: int = Field(..., ge=1, le=118, description="Atomic number (1-118)")
    info: Optional[str] = Field(None, max_length=500, description="Description/information about the element")
    
    @validator('symbol')
    def symbol_must_be_valid(cls, v):
        """Validate that symbol contains only letters"""
        if not v.isalpha():
            raise ValueError('Symbol must contain only letters')
        return v.upper()  # Convert to uppercase for consistency
    
    @validator('name')
    def name_must_be_valid(cls, v):
        """Validate that name contains only letters and spaces"""
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only letters and spaces')
        return v.title()  # Convert to title case for consistency

class ElementCreate(ElementBase):
    """
    Schema for creating a new element
    Used in POST /elements endpoint
    """
    pass

class ElementUpdate(BaseModel):
    """
    Schema for updating an existing element
    Used in PUT /elements/{symbol} endpoint
    All fields are optional for partial updates
    """
    symbol: Optional[str] = Field(None, min_length=1, max_length=10, description="Chemical symbol")
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Full element name")
    number: Optional[int] = Field(None, ge=1, le=118, description="Atomic number")
    info: Optional[str] = Field(None, max_length=500, description="Description/information")
    
    @validator('symbol')
    def symbol_must_be_valid(cls, v):
        """Validate that symbol contains only letters"""
        if v is not None and not v.isalpha():
            raise ValueError('Symbol must contain only letters')
        return v.upper() if v else v
    
    @validator('name')
    def name_must_be_valid(cls, v):
        """Validate that name contains only letters and spaces"""
        if v is not None and not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only letters and spaces')
        return v.title() if v else v

class ElementResponse(ElementBase):
    """
    Schema for element responses
    Used in GET endpoints to return element data
    Includes the database ID field
    """
    id: int = Field(..., description="Database ID")
    
    class Config:
        """Pydantic configuration for the response model"""
        from_attributes = True  # Allows conversion from SQLAlchemy models

class ElementCreateResponse(BaseModel):
    """
    Schema for element creation response
    Used in POST /elements endpoint to return success message and element data
    """
    message: str = Field(..., description="Success message")
    element: ElementResponse = Field(..., description="Created element data")

class ElementUpdateResponse(BaseModel):
    """
    Schema for element update response
    Used in PUT /elements/{symbol} endpoint to return success message and element data
    """
    message: str = Field(..., description="Success message")
    element: ElementResponse = Field(..., description="Updated element data")

class ElementDeleteResponse(BaseModel):
    """
    Schema for element deletion response
    Used in DELETE /elements/{symbol} endpoint to return success message
    """
    message: str = Field(..., description="Success message")
    symbol: str = Field(..., description="Deleted element symbol")

class ErrorResponse(BaseModel):
    """
    Schema for error responses
    Used to return consistent error messages
    """
    detail: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type of error")

# User Authentication Schemas

class UserBase(BaseModel):
    """
    Base schema for user data
    Contains common fields for user operations
    """
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    role: str = Field(default="student", description="User role (admin or student)")

class UserCreate(UserBase):
    """
    Schema for user registration
    Used in POST /register endpoint
    """
    password: str = Field(..., min_length=6, max_length=100, description="Password (6-100 characters)")
    
    @validator('username')
    def username_must_be_valid(cls, v):
        """Validate username contains only alphanumeric characters and underscores"""
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v.lower()  # Convert to lowercase for consistency
    
    @validator('role')
    def role_must_be_valid(cls, v):
        """Validate role is either admin or student"""
        if v not in ["admin", "student"]:
            raise ValueError('Role must be either "admin" or "student"')
        return v

class UserLogin(BaseModel):
    """
    Schema for user login
    Used in POST /login endpoint
    """
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

class UserResponse(UserBase):
    """
    Schema for user responses
    Used to return user data without password
    """
    id: int = Field(..., description="User ID")
    
    class Config:
        """Pydantic configuration for the response model"""
        from_attributes = True  # Allows conversion from SQLAlchemy models

class Token(BaseModel):
    """
    Schema for JWT token response
    Used in POST /login endpoint
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")

class TokenData(BaseModel):
    """
    Schema for token data
    Used internally for JWT token validation
    """
    username: Optional[str] = None

class UserRegisterResponse(BaseModel):
    """
    Schema for user registration response
    Used in POST /register endpoint
    """
    message: str = Field(..., description="Success message")
    user: UserResponse = Field(..., description="Created user data")

class LoginResponse(BaseModel):
    """
    Schema for login response
    Used in POST /login endpoint
    """
    message: str = Field(..., description="Success message")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponse = Field(..., description="User data")
