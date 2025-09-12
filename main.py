"""
Periodic Table Web App - Backend API
FastAPI application for serving periodic table element data

Day 2: SQLite database integration with SQLAlchemy ORM
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uvicorn
from datetime import timedelta

# Import our database models and functions
from models import Element, User, get_db, create_tables, init_sample_data, create_admin_user

# Import Pydantic schemas for request/response validation
from schemas import (
    ElementCreate, ElementUpdate, ElementResponse, 
    ElementCreateResponse, ElementUpdateResponse, ElementDeleteResponse,
    UserCreate, UserLogin, UserResponse, UserRegisterResponse, LoginResponse
)

# Import authentication functions
from auth import (
    authenticate_user, create_access_token, get_current_user, 
    get_current_admin_user, create_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create FastAPI app instance
app = FastAPI(
    title="Periodic Table API",
    description="Backend API for the Periodic Table Web App - Day 3.5: Authentication & CRUD",
    version="3.5.0"
)

# Add CORS middleware to allow frontend requests
# This allows JavaScript fetch calls from the frontend to work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """
    Initialize database when the application starts
    
    This function runs once when the server starts up
    It creates the database tables, adds sample data, and creates admin user
    """
    print("🚀 Starting Periodic Table API...")
    print("📊 Initializing database...")
    
    # Create database tables
    create_tables()
    
    # Add sample data
    init_sample_data()
    
    # Create admin user for testing
    create_admin_user()
    
    print("✅ Database initialization complete!")
    print("🌐 API is ready at http://localhost:8000")
    print("👤 Admin user created: username='admin', password='admin123'")

@app.get("/")
async def root():
    """
    Root endpoint - basic API information
    """
    return {
        "message": "Periodic Table API is running!",
        "version": "3.5.0",
        "database": "SQLite with SQLAlchemy ORM",
        "features": "Authentication + Full CRUD operations for elements",
        "authentication": "JWT-based authentication with role-based access control",
        "endpoints": {
            "public": {
                "get_all_elements": "GET /elements",
                "get_element": "GET /elements/{symbol}",
                "register": "POST /register",
                "login": "POST /login"
            },
            "admin_only": {
                "create_element": "POST /elements (requires admin token)",
                "update_element": "PUT /elements/{symbol} (requires admin token)",
                "delete_element": "DELETE /elements/{symbol} (requires admin token)"
            },
            "docs": "/docs"
        }
    }

@app.get("/elements", response_model=List[ElementResponse])
async def get_all_elements(db: Session = Depends(get_db)):
    """
    Get all elements from the periodic table database
    
    Args:
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        List of all elements with their properties from the database
    """
    # Query all elements from the database
    elements = db.query(Element).all()
    return elements

@app.get("/elements/{symbol}", response_model=ElementResponse)
async def get_element_by_symbol(symbol: str, db: Session = Depends(get_db)):
    """
    Get a specific element by its chemical symbol from the database
    
    Args:
        symbol: The chemical symbol of the element (e.g., "H", "He", "C")
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        Element data if found
        
    Raises:
        HTTPException: 404 if element not found
    """
    # Convert symbol to uppercase for case-insensitive search
    symbol_upper = symbol.upper()
    
    # Query database for element with matching symbol (case-insensitive)
    element = db.query(Element).filter(Element.symbol.ilike(symbol_upper)).first()
    
    if element:
        return element
    else:
        # If element not found, raise 404 error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Element with symbol '{symbol}' not found"
        )

# Authentication Endpoints

@app.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account
    
    Args:
        user_data: User registration data (username, password, role)
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        Success message and user data (without password)
        
    Raises:
        HTTPException: 400 if username already exists or validation fails
    """
    try:
        # Create new user
        new_user = create_user(
            db=db,
            username=user_data.username,
            password=user_data.password,
            role=user_data.role
        )
        
        return UserRegisterResponse(
            message=f"User '{new_user.username}' registered successfully",
            user=new_user
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (like username already exists)
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/login", response_model=LoginResponse)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token
    
    Args:
        user_credentials: Username and password
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        JWT token and user information
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        message=f"Login successful for user '{user.username}'",
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user=user
    )

# Protected CRUD Endpoints (Admin Only)

@app.post("/elements", response_model=ElementCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_element(element_data: ElementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """
    Create a new element in the database (Admin Only)
    
    Args:
        element_data: Element data from request body (validated by Pydantic)
        db: Database session (automatically provided by FastAPI)
        current_user: Current authenticated admin user (automatically provided by FastAPI)
    
    Returns:
        Success message and created element data
        
    Raises:
        HTTPException: 400 if element already exists or validation fails
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not admin user
    """
    # Check if element with this symbol already exists
    existing_element = db.query(Element).filter(Element.symbol == element_data.symbol).first()
    if existing_element:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Element with symbol '{element_data.symbol}' already exists"
        )
    
    # Check if element with this atomic number already exists
    existing_number = db.query(Element).filter(Element.number == element_data.number).first()
    if existing_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Element with atomic number '{element_data.number}' already exists"
        )
    
    # Create new element
    new_element = Element(
        symbol=element_data.symbol,
        name=element_data.name,
        number=element_data.number,
        info=element_data.info
    )
    
    # Add to database
    db.add(new_element)
    db.commit()
    db.refresh(new_element)
    
    return ElementCreateResponse(
        message=f"Element '{new_element.symbol}' created successfully",
        element=new_element
    )

@app.put("/elements/{symbol}", response_model=ElementUpdateResponse)
async def update_element(symbol: str, element_data: ElementUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """
    Update an existing element in the database (Admin Only)
    
    Args:
        symbol: The chemical symbol of the element to update
        element_data: Updated element data from request body
        db: Database session (automatically provided by FastAPI)
        current_user: Current authenticated admin user (automatically provided by FastAPI)
    
    Returns:
        Success message and updated element data
        
    Raises:
        HTTPException: 404 if element not found, 400 if validation fails
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not admin user
    """
    # Convert symbol to uppercase for case-insensitive search
    symbol_upper = symbol.upper()
    
    # Find the element to update
    element = db.query(Element).filter(Element.symbol.ilike(symbol_upper)).first()
    if not element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Element with symbol '{symbol}' not found"
        )
    
    # Check if new symbol conflicts with existing element
    if element_data.symbol and element_data.symbol != element.symbol:
        existing_symbol = db.query(Element).filter(Element.symbol == element_data.symbol).first()
        if existing_symbol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Element with symbol '{element_data.symbol}' already exists"
            )
    
    # Check if new atomic number conflicts with existing element
    if element_data.number and element_data.number != element.number:
        existing_number = db.query(Element).filter(Element.number == element_data.number).first()
        if existing_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Element with atomic number '{element_data.number}' already exists"
            )
    
    # Update element fields (only update provided fields)
    if element_data.symbol is not None:
        element.symbol = element_data.symbol
    if element_data.name is not None:
        element.name = element_data.name
    if element_data.number is not None:
        element.number = element_data.number
    if element_data.info is not None:
        element.info = element_data.info
    
    # Save changes to database
    db.commit()
    db.refresh(element)
    
    return ElementUpdateResponse(
        message=f"Element '{element.symbol}' updated successfully",
        element=element
    )

@app.delete("/elements/{symbol}", response_model=ElementDeleteResponse)
async def delete_element(symbol: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """
    Delete an element from the database (Admin Only)
    
    Args:
        symbol: The chemical symbol of the element to delete
        db: Database session (automatically provided by FastAPI)
        current_user: Current authenticated admin user (automatically provided by FastAPI)
    
    Returns:
        Success message and deleted element symbol
        
    Raises:
        HTTPException: 404 if element not found
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not admin user
    """
    # Convert symbol to uppercase for case-insensitive search
    symbol_upper = symbol.upper()
    
    # Find the element to delete
    element = db.query(Element).filter(Element.symbol.ilike(symbol_upper)).first()
    if not element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Element with symbol '{symbol}' not found"
        )
    
    # Store symbol for response before deletion
    deleted_symbol = element.symbol
    
    # Delete element from database
    db.delete(element)
    db.commit()
    
    return ElementDeleteResponse(
        message=f"Element '{deleted_symbol}' deleted successfully",
        symbol=deleted_symbol
    )

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy", "message": "API is running"}

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
