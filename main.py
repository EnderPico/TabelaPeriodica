"""
Periodic Table Web App - Backend API
FastAPI application for serving periodic table element data

This is Day 1 setup - basic API with mock data
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn

# Create FastAPI app instance
app = FastAPI(
    title="Periodic Table API",
    description="Backend API for the Periodic Table Web App",
    version="1.0.0"
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

# Mock data for elements - this will be replaced with database in Day 2
MOCK_ELEMENTS = [
    {
        "atomic_number": 1,
        "symbol": "H",
        "name": "Hydrogen",
        "atomic_mass": 1.008,
        "period": 1,
        "group": 1,
        "category": "Nonmetal",
        "description": "The lightest and most abundant element in the universe. Essential for water and organic compounds.",
        "electron_configuration": "1s¹",
        "melting_point": -259.16,
        "boiling_point": -252.87,
        "density": 0.00008988
    },
    {
        "atomic_number": 6,
        "symbol": "C",
        "name": "Carbon",
        "atomic_mass": 12.011,
        "period": 2,
        "group": 14,
        "category": "Nonmetal",
        "description": "The basis of all organic life. Forms millions of compounds and is essential for life on Earth.",
        "electron_configuration": "[He] 2s² 2p²",
        "melting_point": 3500,
        "boiling_point": 4027,
        "density": 2.267
    },
    {
        "atomic_number": 8,
        "symbol": "O",
        "name": "Oxygen",
        "atomic_mass": 15.999,
        "period": 2,
        "group": 16,
        "category": "Nonmetal",
        "description": "Essential for respiration and combustion. Makes up about 21% of Earth's atmosphere.",
        "electron_configuration": "[He] 2s² 2p⁴",
        "melting_point": -218.79,
        "boiling_point": -182.95,
        "density": 1.429
    }
]

@app.get("/")
async def root():
    """
    Root endpoint - basic API information
    """
    return {
        "message": "Periodic Table API is running!",
        "version": "1.0.0",
        "endpoints": {
            "elements": "/elements",
            "element_by_symbol": "/elements/{symbol}",
            "docs": "/docs"
        }
    }

@app.get("/elements", response_model=List[Dict[str, Any]])
async def get_all_elements():
    """
    Get all elements from the periodic table
    
    Returns:
        List of all elements with their properties
    """
    return MOCK_ELEMENTS

@app.get("/elements/{symbol}", response_model=Dict[str, Any])
async def get_element_by_symbol(symbol: str):
    """
    Get a specific element by its chemical symbol
    
    Args:
        symbol: The chemical symbol of the element (e.g., "H", "C", "O")
    
    Returns:
        Element data if found
        
    Raises:
        HTTPException: 404 if element not found
    """
    # Convert symbol to uppercase for case-insensitive search
    symbol_upper = symbol.upper()
    
    # Search for element by symbol
    for element in MOCK_ELEMENTS:
        if element["symbol"].upper() == symbol_upper:
            return element
    
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
