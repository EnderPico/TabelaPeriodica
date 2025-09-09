# Periodic Table Web App - Backend

A FastAPI backend for a high school IT class project featuring an interactive periodic table with flip cards, element information, and future chat/AI integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd TabelaPeriodica
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**:
   - API Base URL: http://localhost:8000
   - Interactive API Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## 📚 API Endpoints

### Day 1 - Basic Element Data

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/elements` | Get all elements (currently 3 mock elements) |
| GET | `/elements/{symbol}` | Get specific element by symbol (e.g., "H", "C", "O") |
| GET | `/health` | Health check endpoint |

### Example API Responses

**Get all elements** (`GET /elements`):
```json
[
  {
    "atomic_number": 1,
    "symbol": "H",
    "name": "Hydrogen",
    "atomic_mass": 1.008,
    "period": 1,
    "group": 1,
    "category": "Nonmetal",
    "description": "The lightest and most abundant element...",
    "electron_configuration": "1s¹",
    "melting_point": -259.16,
    "boiling_point": -252.87,
    "density": 0.00008988
  }
]
```

**Get specific element** (`GET /elements/H`):
```json
{
  "atomic_number": 1,
  "symbol": "H",
  "name": "Hydrogen",
  "atomic_mass": 1.008,
  "period": 1,
  "group": 1,
  "category": "Nonmetal",
  "description": "The lightest and most abundant element...",
  "electron_configuration": "1s¹",
  "melting_point": -259.16,
  "boiling_point": -252.87,
  "density": 0.00008988
}
```

## 🔗 Frontend Integration

### JavaScript Fetch Examples

**Get all elements**:
```javascript
async function fetchAllElements() {
    try {
        const response = await fetch('http://localhost:8000/elements');
        const elements = await response.json();
        console.log('All elements:', elements);
        return elements;
    } catch (error) {
        console.error('Error fetching elements:', error);
    }
}
```

**Get specific element**:
```javascript
async function fetchElement(symbol) {
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`);
        if (response.ok) {
            const element = await response.json();
            console.log('Element data:', element);
            return element;
        } else {
            console.error('Element not found');
        }
    } catch (error) {
        console.error('Error fetching element:', error);
    }
}

// Usage examples:
fetchElement('H');  // Get Hydrogen
fetchElement('C');  // Get Carbon
fetchElement('O');  // Get Oxygen
```

## 📅 Development Roadmap

- **Day 1** ✅: Basic API with mock data (CURRENT)
- **Day 2**: SQLite database integration with real periodic table data
- **Day 3**: User login and authentication system
- **Day 4**: CRUD operations for updating element information
- **Day 5**: Chat/AI bot integration
- **Day 6**: Integration testing and polish
- **Day 7**: Presentation preparation

## 🛠️ Development Commands

```bash
# Run development server with auto-reload
uvicorn main:app --reload

# Run on specific host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

## 📁 Project Structure

```
TabelaPeriodica/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🤝 Team Collaboration

This backend is designed to work with the frontend team's HTML/CSS/JS implementation. The API provides clean JSON responses that can be easily consumed by JavaScript fetch calls.

**For Frontend Developers**: Use the JavaScript examples above to integrate with this API. The CORS middleware is configured to allow requests from any origin during development.

## 🐛 Troubleshooting

**Port already in use**:
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001 --reload
```

**Module not found errors**:
```bash
# Make sure you're in the project directory
cd TabelaPeriodica

# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 Notes

- This is Day 1 implementation with mock data
- CORS is configured for development (allows all origins)
- Database integration will be added in Day 2
- Authentication will be added in Day 3
