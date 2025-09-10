"""
Periodic Table Web App - Backend API
FastAPI application for serving periodic table element data

Day 2: SQLite database integration with SQLAlchemy ORM
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uvicorn

# Import our database models and functions
from models import Element, get_db, create_tables, init_sample_data

# Create FastAPI app instance
app = FastAPI(
    title="Periodic Table API",
    description="Backend API for the Periodic Table Web App - Day 2: Database Integration",
    version="2.0.0"
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
        "version": "2.0.0",
        "database": "SQLite with SQLAlchemy ORM",
        "endpoints": {
            "elements": "/elements",
            "element_by_symbol": "/elements/{symbol}",
            "docs": "/docs"
        }
    }

@app.get("/elements", response_model=List[Dict[str, Any]])
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
    
    # Convert SQLAlchemy objects to dictionaries for JSON response
    return [element.to_dict() for element in elements]

@app.get("/elements/{symbol}", response_model=Dict[str, Any])
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
        return element.to_dict()
    else:
        # If element not found, raise 404 error
        raise HTTPException(
            status_code=404, 
            detail=f"Element with symbol '{symbol}' not found"
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
