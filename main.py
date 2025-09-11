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

# Import our database models and functions
from models import Element, get_db, create_tables, init_sample_data

# Import Pydantic schemas for request/response validation
from schemas import (
    ElementCreate, ElementUpdate, ElementResponse, 
    ElementCreateResponse, ElementUpdateResponse, ElementDeleteResponse
)

# Create FastAPI app instance
app = FastAPI(
    title="Periodic Table API",
    description="Backend API for the Periodic Table Web App - Day 3.9: CRUD Operations",
    version="3.9.0"
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
    It creates the database tables and adds sample data
    """
    print("🚀 Starting Periodic Table API...")
    print("📊 Initializing database...")
    
    # Create database tables
    create_tables()
    
    # Add sample data
    init_sample_data()
    
    print("✅ Database initialization complete!")
    print("🌐 API is ready at http://localhost:8000")

@app.get("/")
async def root():
    """
    Root endpoint - basic API information
    """
    return {
        "message": "Periodic Table API is running!",
        "version": "3.9.0",
        "database": "SQLite with SQLAlchemy ORM",
        "features": "Full CRUD operations for elements",
        "endpoints": {
            "get_all_elements": "GET /elements",
            "get_element": "GET /elements/{symbol}",
            "create_element": "POST /elements",
            "update_element": "PUT /elements/{symbol}",
            "delete_element": "DELETE /elements/{symbol}",
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

@app.post("/elements", response_model=ElementCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_element(element_data: ElementCreate, db: Session = Depends(get_db)):
    """
    Create a new element in the database
    
    Args:
        element_data: Element data from request body (validated by Pydantic)
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        Success message and created element data
        
    Raises:
        HTTPException: 400 if element already exists or validation fails
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
async def update_element(symbol: str, element_data: ElementUpdate, db: Session = Depends(get_db)):
    """
    Update an existing element in the database
    
    Args:
        symbol: The chemical symbol of the element to update
        element_data: Updated element data from request body
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        Success message and updated element data
        
    Raises:
        HTTPException: 404 if element not found, 400 if validation fails
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
async def delete_element(symbol: str, db: Session = Depends(get_db)):
    """
    Delete an element from the database
    
    Args:
        symbol: The chemical symbol of the element to delete
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        Success message and deleted element symbol
        
    Raises:
        HTTPException: 404 if element not found
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
