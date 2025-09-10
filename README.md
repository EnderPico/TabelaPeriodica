# Periodic Table Web App - Backend

A FastAPI backend for a high school IT class project featuring an interactive periodic table with flip cards, element information, and future chat/AI integration.

**Day 2 Update**: Now includes SQLite database integration with SQLAlchemy ORM for persistent element data storage.

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

### Database Setup

The SQLite database is automatically created and initialized when you first run the server. No additional setup required!

- **Database file**: `periodic_table.db` (created in project directory)
- **Sample data**: Automatically includes Hydrogen and Helium
- **Management**: Use `python manage_db.py` to add more elements

## 📚 API Endpoints

### Day 2 - Database Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/elements` | Get all elements from SQLite database |
| GET | `/elements/{symbol}` | Get specific element by symbol (e.g., "H", "He") |
| GET | `/health` | Health check endpoint |

### Example API Responses

**Get all elements** (`GET /elements`):
```json
[
  {
    "id": 1,
    "symbol": "H",
    "name": "Hydrogen",
    "number": 1,
    "info": "The lightest and most abundant element in the universe. Essential for water and organic compounds."
  },
  {
    "id": 2,
    "symbol": "He",
    "name": "Helium",
    "number": 2,
    "info": "A noble gas that is lighter than air. Used in balloons and as a coolant for superconducting magnets."
  }
]
```

**Get specific element** (`GET /elements/H`):
```json
{
  "id": 1,
  "symbol": "H",
  "name": "Hydrogen",
  "number": 1,
  "info": "The lightest and most abundant element in the universe. Essential for water and organic compounds."
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

- **Day 1** ✅: Basic API with mock data
- **Day 2** ✅: SQLite database integration with real periodic table data (CURRENT)
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
├── models.py            # SQLAlchemy database models
├── manage_db.py         # Database management script
├── test_api.py          # API testing script
├── requirements.txt     # Python dependencies
├── periodic_table.db    # SQLite database (created automatically)
└── README.md           # This file
```

## 🗄️ Database Management

### Adding Elements

Use the database management script to add more elements:

```bash
python manage_db.py
```

This interactive script allows you to:
- Add sample elements (Lithium, Carbon, Nitrogen, Oxygen, Fluorine)
- Add custom elements with your own data
- List all elements in the database
- Reset the database if needed

### Adding Elements Programmatically

You can also add elements directly in Python:

```python
from models import add_element

# Add a new element
add_element(
    symbol="Na",
    name="Sodium", 
    number=11,
    info="Essential for nerve function and muscle contraction."
)
```

### Database Schema

The `Element` table has the following structure:
- `id`: Primary key (auto-increment)
- `symbol`: Chemical symbol (unique, e.g., "H", "He")
- `name`: Full element name (e.g., "Hydrogen", "Helium")
- `number`: Atomic number (e.g., 1, 2)
- `info`: Description/information about the element

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

- This is Day 2 implementation with SQLite database integration
- CORS is configured for development (allows all origins)
- Database is automatically created and initialized on first run
- Case-insensitive element symbol search (e.g., "h", "H", "he", "He" all work)
- Authentication will be added in Day 3
- Use `python manage_db.py` to easily add more elements
- SQLAlchemy 2.0.43 for Python 3.13 compatibility
