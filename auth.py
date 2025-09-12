"""
Authentication and Authorization Module
Handles password hashing, JWT token creation, and user authentication

This module provides secure authentication functions for the Periodic Table API
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Import our database models
from models import User, get_db

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expires after 30 minutes

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password from database
    
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password (str): The plain text password to hash
    
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data (dict): The data to encode in the token (usually user info)
        expires_delta (Optional[timedelta]): Token expiration time
    
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    
    # Set token expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Encode the token with secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token
    
    Args:
        token (str): The JWT token to verify
    
    Returns:
        Optional[dict]: The decoded token data if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password
    
    Args:
        db (Session): Database session
        username (str): Username to authenticate
        password (str): Plain text password
    
    Returns:
        Optional[User]: User object if authentication successful, None otherwise
    """
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
    
    # Check if user exists and password is correct
    if user and verify_password(password, user.password_hash):
        return user
    
    return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get the current authenticated user from JWT token
    
    This is a FastAPI dependency that can be used in protected endpoints
    
    Args:
        token (str): JWT token from Authorization header
        db (Session): Database session
    
    Returns:
        User: The authenticated user
    
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # "sub" is the standard JWT field for subject (username)
        
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current user and verify they have admin role
    
    This is a FastAPI dependency for admin-only endpoints
    
    Args:
        current_user (User): The current authenticated user
    
    Returns:
        User: The authenticated admin user
    
    Raises:
        HTTPException: 403 if user is not an admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )
    
    return current_user

def create_user(db: Session, username: str, password: str, role: str = "student") -> User:
    """
    Create a new user in the database
    
    Args:
        db (Session): Database session
        username (str): Username for the new user
        password (str): Plain text password (will be hashed)
        role (str): User role (default: "student")
    
    Returns:
        User: The created user object
    
    Raises:
        HTTPException: 400 if username already exists
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        password_hash=hashed_password,
        role=role
    )
    
    # Add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
